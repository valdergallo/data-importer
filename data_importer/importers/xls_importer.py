#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseImporter
from data_importer.readers import XLSReader


class XLSImporter(BaseImporter):

    def set_reader(self):
        '''
            [[1,2,3], [2,3,4]]
        '''
        sheet_by_name = self.Meta.sheet_name or None
        sheet_by_index = self.Meta.sheet_index or 0

        self._reader = XLSReader(self, sheet_name=sheet_by_name, sheet_index=sheet_by_index)

