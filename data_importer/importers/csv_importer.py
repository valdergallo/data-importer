# encoding: utf-8
from __future__ import unicode_literals
from data_importer.importers.base import BaseImporter
from data_importer.readers import CSVReader


class CSVImporter(BaseImporter):

    def set_reader(self):
        delimiter = self.Meta.delimiter or ';'
        delimiter = str(delimiter)
        self._reader = CSVReader(self, delimiter=delimiter)
