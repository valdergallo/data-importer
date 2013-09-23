#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
from django.db import transaction
from django.utils.encoding import force_unicode

from data_importer import default_settings
from data_importer.importers.descriptor import ReadDescriptor
from data_importer.exceptions import StopImporter


DATA_IMPORTER_EXCEL_DECODER = default_settings.DATA_IMPORTER_EXCEL_DECODER

DATA_IMPORTER_DECODER = default_settings.DATA_IMPORTER_DECODER


def objclass2dict(objclass):
    """
    Meta is a objclass on python 2.7 and no have __dict__ attribute.

    This method convert one objclass to one lazy dict without AttributeError
    """
    class Dict(dict):
        def __init__(self, data={}):
            super(Dict, self).__init__(data)
            self.__dict__ = dict(self.items())

        def __getattr__(self, key):
            try:
                return self.__getattribute__(key)
            except AttributeError:
                return False

    obj_list = [i for i in dir(objclass) if not str(i).startswith("__")]
    obj_values = []
    for objitem in obj_list:
        obj_values.append(getattr(objclass, objitem))
    return Dict(zip(obj_list, obj_values))


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

    def __init__(self, source=None):
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
        descriptor = ReadDescriptor(self.Meta.descriptor, self.Meta.model)
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
        self._reader = csv.reader(self.source, delimiter=self.meta.get('delimiter', ';'))

    def process_row(self, row, values):
        """
        Read clean functions from importer and return tupla with row number, field and value
        """
        values_encoded = [self.to_unicode(i) for i in values]
        values = dict(zip(self.fields, values_encoded))
        for k, v in values.items():
            if hasattr(self, 'clean_%s' % k):
                clean_function = getattr(self, 'clean_%s' % k)

                if self.Meta.raise_errors:
                    values[k] = clean_function(v)
                else:
                    try:
                        values[k] = clean_function(v)
                    except StopImporter, e:
                        raise StopImporter((row, type(e).__name__, unicode(e)))
                    except Exception, e:
                        self._error.append((row, type(e).__name__, unicode(e)))

        return (row, values)

    @property
    def cleaned_data(self):
        """
        Return tupla with data cleaned
        """
        if self._readed:
            return self._cleaned_data

        try:
            self.pre_clean()
        except Exception, e:
            self._error.append(('__pre_clean__', repr(e)))

        # create clean content
        for data in self._read_file():
            self._cleaned_data += (data, )

        try:
            self.clean()
        except Exception, e:
            self._error.append(('__clean_all__', repr(e)))

        try:
            self.post_clean()
        except Exception, e:
            self._error.append(('__post_clean__', repr(e)))

        self._readed = True
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
        for row, values in enumerate(self._reader):
            if self.Meta.ignore_first_line:
                row -= 1
            if row == -1:
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
            raise AttributeError("Invalid instance model")

        if self.Meta.transaction:
            with transaction.atomic():
                for row, data in self.cleaned_data:
                    record = instance(**data)
                    record.save()

                try:
                    self.pre_commit()
                except Exception, e:
                    self._error.append(('__pre_commit__', repr(e)))
                    transaction.rollback()

                try:
                    transaction.commit()
                except Exception, e:
                    self._error.append(('__trasaction__', repr(e)))
                    transaction.rollback()

        else:
            for row, data in self.cleaned_data:
                record = instance(**data)
                record.save()

        self.post_save_all_lines()

        return True
