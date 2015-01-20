# -*- coding: utf-8 -*-
from data_importer.readers.xls_reader import XLSReader
from data_importer.readers.xlsx_reader import XLSXReader
from data_importer.readers.csv_reader import CSVReader
from data_importer.readers.xml_reader import XMLReader
from data_importer.core.exceptions import UnsuportedFile
from .base import BaseImporter


class GenericImporter(BaseImporter):
    """
    An implementation of BaseImporter that sets the right reader
    by file extension.
    Probably the best choice for almost all implementation cases
    """
    def set_reader(self):
        reader = self.get_reader_class()

        # default importers configurations
        extra_values = {
            'xlsx': {'user_iterator': True, 'data_only': True},
            'xls': {'sheet_name': self.Meta.sheet_name or None, 'sheet_index': self.Meta.sheet_index or 0},
            'csv': {'delimiter': self.Meta.delimiter or ';'},
            'xml': {},
        }

        selected_extra_values = extra_values[self.get_source_file_extension()]
        self._reader = reader(self, **selected_extra_values)

    def get_reader_class(self):
        """
        Gets the right file reader class by source file extension
        """
        readers = {
            'xls': XLSReader,
            'xlsx': XLSXReader,
            'xml': XMLReader,
            'csv': CSVReader,
            }
        source_file_extension = self.get_source_file_extension()

        # No reader for invalid extensions
        if source_file_extension not in readers.keys():
            raise UnsuportedFile("Unsuported File")

        return readers[source_file_extension]

    def get_source_file_extension(self):
        """
        Gets the source file extension. Used to choose the right reader
        """
        if hasattr(self.source, 'file') and hasattr(self.source.file, 'name'):
            filename = self.source.file.name # File instances
        elif hasattr(self.source, 'file_upload'):
            if hasattr(self.source.file_upload, 'name'):
                filename = self.source.file_upload.name  # Default DataImporter.models.FileUploadHistory
            else:
                filename = self.source.file_upload
        elif hasattr(self.source, 'name'):
            filename = self.source.name  # Default filename
        else:
            filename = self.source

        ext = filename.split('.')[-1]
        return ext.lower()
