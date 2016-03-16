#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data_importer.importers.base import BaseImporter
from data_importer.readers import XLSHTMLReader


class XLSHTMLImporter(BaseImporter):
    table_selector = 'table'

    def set_reader(self):
        self._reader = XLSHTMLReader(self)
