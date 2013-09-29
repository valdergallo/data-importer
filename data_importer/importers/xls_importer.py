#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import xlrd
from .base import BaseImporter

#from xlrd/biffh.py
# (
#     XL_CELL_EMPTY,
#     XL_CELL_TEXT,
#     XL_CELL_NUMBER,
#     XL_CELL_DATE,
#     XL_CELL_BOOLEAN,
#     XL_CELL_ERROR,
#     XL_CELL_BLANK,  # for use in debugging, gathering stats, etc
# ) = range(7)


class XLSImporter(BaseImporter):

    def set_reader(self, on_demand=True):
        self.workbook = xlrd.open_workbook(self.source, on_demand=on_demand)
        if self.Meta.sheet_name:
            self.worksheet = self.workbook.sheet_by_name(self.Meta.sheet_name)
        else:
            self.worksheet = self.workbook.sheet_by_index(0)

        self._reader = self.get_items()

    def convert_value(self, item):
        """
        Handle different value types for XLS. Item is a cell object.
        """
        # Thx to Augusto C Men to point fast solution for XLS/XLSX dates
        if item.ctype == 3: #XL_CELL_DATE:
            return datetime.datetime(*xlrd.xldate_as_tuple(item.value, self.workbook.datemode))

        if item.ctype == 2: #XL_CELL_NUMBER:
            if item.value % 1 == 0:  # integers
                return int(item.value)
            else:
                return item.value

        return item.value

    def get_items(self):
        """
        Get values from cells
        :return: generator
        """
        for i in xrange(0, self.worksheet.nrows):
            values = [self.convert_value(cell) for cell in self.worksheet.row(i)]
            if not any(values):
                continue  # empty lines are ignored
            yield values

