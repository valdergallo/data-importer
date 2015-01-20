#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from django.db import transaction
from django.db.models.fields import FieldDoesNotExist
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode
from data_importer.core.descriptor import ReadDescriptor
from data_importer.core.exceptions import StopImporter
from data_importer.core.base import objclass2dict
from data_importer.core.base import DATA_IMPORTER_EXCEL_DECODER
from data_importer.core.base import DATA_IMPORTER_DECODER


class BaseImporter(object):
    """
    Base Importer method to create simples importes CSV files.

    set_reader: can be override to create new importers files
    """
    def __new__(cls, **kargs):
        """
        Provide custom methods in subclass Meta
        """
        if hasattr(cls, "Meta"):
            cls.Meta = objclass2dict(cls.Meta)
        return super(BaseImporter, cls).__new__(cls)

    def __init__(self, source=None, *args, **kwargs):
        self.file_history = None
        self._fields = []
        self._error = []
        self._cleaned_data = ()
        self._reader = None
        self._excluded = False
        self._readed = False

        self.start_fields()
        if source:
            self.source = source
            self.set_reader()

    class Meta:
        """
        Importer configurations
        """

    @staticmethod
    def to_unicode(bytestr):
        """
        Receive string bytestr and try to return a utf-8 string.
        """
        if not isinstance(bytestr, str) and not isinstance(bytestr, unicode):
            return bytestr

        try:
            decoded = bytestr.decode(DATA_IMPORTER_EXCEL_DECODER)  # default by excel csv
        except UnicodeEncodeError:
            decoded = force_unicode(bytestr, DATA_IMPORTER_DECODER)

        return decoded

    @property
    def source(self):
        """
        Return source opened
        """
        return self._source

    @source.setter
    def source(self, source):
        """
        Open source to reader
        """
        if isinstance(source, file):
            self._source = source
        elif isinstance(source, str) and os.path.exists(source) and source.endswith('csv'):
            self._source = open(source, 'rb')
        elif isinstance(source, list):
            self._source = source
        elif hasattr(source, 'file_upload'):  # for FileHistory instances
            self._source = source.file_upload
            self.file_history = source
        elif hasattr(source, 'file'):
            self._source = open(source.file.name, 'rb')
        else:
            self._source = source
            # raise ValueError('Invalid Source')

    @property
    def meta(self):
        """
        Is same to use .Meta
        """
        if hasattr(self, 'Meta'):
            return self.Meta

    def start_fields(self):
        """
        Initial function to find fields or headers values
        This values will be used to process clean and save method
        If this method not have fields and have Meta.model this method
        will use model fields to populate content without id
        """
        if self.Meta.model and not hasattr(self, 'fields'):
            all_models_fields = [i.name for i in self.Meta.model._meta.fields if i.name != 'id']
            self.fields = all_models_fields

        self.exclude_fields()

        if self.Meta.descriptor:
            self.load_descriptor()

    def exclude_fields(self):
        """
        Exclude fields from Meta.exclude
        """
        if self.Meta.exclude and not self._excluded:
            self._excluded = True
            for exclude in self.Meta.exclude:
                if exclude in self.fields:
                    self.fields.remove(exclude)

    def load_descriptor(self):
        """
        Set fields from descriptor file
        """
        descriptor = ReadDescriptor(self.Meta.descriptor, self.Meta.descriptor_model)
        self.fields = descriptor.get_fields()
        self.exclude_fields()

    @property
    def errors(self):
        """
        Show errors catch by clean methods
        """
        return self._error

    def is_valid(self):
        """
        Clear content and return False if have errors
        """
        if not self.cleaned_data:
            self.cleaned_data
        return not any(self._error)

    def set_reader(self):
        """
        Method responsable to convert file content into a list with same values that
        have fields

            fields: ['myfield1', 'myfield2']

            response: [['value_myfield1', 'value_myfield2'],
                        ['value2_myfield1', 'value2_myfield2']]
        """
        raise NotImplementedError('No reader implemented')

    def clean_field(self, field_name, value):
        """
        User default django field validators to clean content
        and run custom validates
        """
        if self.Meta.model:
            # default django validate field
            try:
                field = self.Meta.model._meta.get_field(field_name)
                field.clean(value, field)
            except FieldDoesNotExist:
                pass  # do nothing if not find this field in model
            except ValidationError as msg:
                default_msg = msg.messages[0].replace('This field', '')
                new_msg = u'Field (%s) %s' % (field.name, default_msg)
                raise ValidationError(new_msg)

        clean_function = getattr(self, 'clean_%s' % field_name, False)

        if clean_function:
            return clean_function(value)
        return value

    def process_row(self, row, values):
        """
        Read clean functions from importer and return tupla with row number, field and value
        """
        values_encoded = [self.to_unicode(i) for i in values]
        try:
            values = dict(zip(self.fields, values_encoded))
        except TypeError:
            raise TypeError('Invalid Line: %s' % row)

        has_error = False

        if self.Meta.ignore_empty_lines:
            # ignore empty lines
            if not any(values.values()):
                return None

        for k, v in values.items():
            if self.Meta.raise_errors:
                values[k] = self.clean_field(k, v)
            else:
                try:
                    values[k] = self.clean_field(k, v)
                except StopImporter, e:
                    raise StopImporter(self.get_error_message(e, row))
                except Exception, e:
                    self._error.append(self.get_error_message(e, row))
                    has_error = True

        if has_error:
            return None

        # validate full row data
        try:
            values = self.clean_row(values)
        except Exception, e:
            self._error.append(self.get_error_message(e, row))
            return None

        return (row, values)

    def get_error_message(self, error, row=None, error_type=None):
        messages = error

        if not error_type:
            error_type = u"%s" % type(error).__name__

        if hasattr(error, 'message'):
            if error.message:
                messages = u'%s' % error.message
        elif hasattr(error, 'messages'):
            if error.messages:
                messages = u','.join(error.messages)

        messages = re.sub('\'', '', messages)
        error_type = re.sub('\'', '', error_type)

        if row:
            return row, error_type, messages
        else:
            return error_type, messages

    @property
    def cleaned_data(self):
        """
        Return tupla with data cleaned
        """
        if self._readed:
            return self._cleaned_data

        self._readed = True

        try:
            self.pre_clean()
        except Exception, e:
            self._error.append(self.get_error_message(e, error_type='__pre_clean__'))

        try:
            self.clean()
        except Exception, e:
            self._error.append(self.get_error_message(e, error_type='__clean_all__'))

        # create clean content
        for data in self._read_file():
            if data:
                self._cleaned_data += (data, )

        try:
            self.post_clean()
        except Exception, e:
            self._error.append(self.get_error_message(e, error_type='__post_clean__'))

        return self._cleaned_data

    def pre_clean(self):
        """
        Executed before all clean methods
        Important: pre_clean dont have cleaned_data content
        """

    def post_clean(self):
        """
        Excuted after all clean method
        """

    def clean(self):
        """
        Custom clean method
        """

    def clean_row(self, row_values):
        """
        Custom clean method for full row data
        """
        return row_values

    def pre_commit(self):
        """
        Executed before commit multiple register
        """

    def post_save_all_lines(self):
        """
        End exection
        """

    def _read_file(self):
        """
        Create cleaned_data content
        """

        if hasattr(self._reader, 'read'):
            reader = self._reader.read()
        else:
            reader = self._reader

        for row, values in enumerate(reader, 1):
            if self.Meta.ignore_first_line:
                row -= 1
            if self.Meta.starting_row and row < self.Meta.starting_row:
                pass
            elif row < 1:
                pass
            else:
                yield self.process_row(row, values)

    def save(self, instance=None):
        """
        Save all contents
        DONT override this method
        """
        if not instance:
            instance = self.Meta.model

        if not instance:
            raise AttributeError('Invalid instance model')

        if self.Meta.transaction:
            with transaction.atomic():
                for row, data in self.cleaned_data:
                    record = instance(**data)
                    record.save()

                try:
                    self.pre_commit()
                except Exception, e:
                    self._error.append(self.get_error_message(e, error_type='__pre_commit__'))
                    transaction.rollback()

                try:
                    transaction.commit()
                except Exception, e:
                    self._error.append(self.get_error_message(e, error_type='__trasaction__'))
                    transaction.rollback()

        else:
            for row, data in self.cleaned_data:
                record = instance(**data)
                record.save(force_update=False)

        self.post_save_all_lines()

        return True
