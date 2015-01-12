#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import xlrd
from django.db.models.fields.files import FieldFile
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


class XLSReader(object):

    def __init__(self, instance, sheet_name=None, sheet_index=0, on_demand=True):

        if isinstance(instance.source, FieldFile):
            source = instance.source.path
        else:
            source = instance.source

        self.workbook = xlrd.open_workbook(source, on_demand=on_demand)

        if sheet_name:
            self.worksheet = self.workbook.sheet_by_name(instance.Meta.sheet_name)
        else:
            self.worksheet = self.workbook.sheet_by_index(sheet_index)

    @staticmethod
    def convert_value(item, workbook):
        """
        Handle different value types for XLS. Item is a cell object.
        """
        # Thx to Augusto C Men to point fast solution for XLS/XLSX dates
        if item.ctype == 3:  # XL_CELL_DATE:
            return datetime.datetime(*xlrd.xldate_as_tuple(item.value, workbook.datemode))

        if item.ctype == 2:  # XL_CELL_NUMBER:
            if item.value % 1 == 0:  # integers
                return int(item.value)
            else:
                return item.value

        return item.value

    def read(self):
        for i in xrange(0, self.worksheet.nrows):
            values = [self.convert_value(cell, self.workbook) for cell in self.worksheet.row(i)]
            yield values
