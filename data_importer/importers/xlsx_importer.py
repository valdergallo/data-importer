#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data_importer.importers.base import BaseImporter
from data_importer.readers.xlsx_reader import XLSXReader


class XLSXImporter(BaseImporter):

    def set_reader(self, data_only=True):
        "Read XLSX files"
        self._reader = XLSXReader(self, data_only=True)
