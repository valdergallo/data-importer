#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data_importer.importers.base import BaseImporter
from data_importer.readers import CSVReader


class CSVImporter(BaseImporter):

    def set_reader(self):
        delimiter = self.Meta.delimiter or ';'
        self._reader = CSVReader(self, delimiter=delimiter)
