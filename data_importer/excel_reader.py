# coding: utf-8
import datetime
import xlrd
import openpyxl
from base import BaseImporter

#from xlrd/biffh.py
(
    XL_CELL_EMPTY,
    XL_CELL_TEXT,
    XL_CELL_NUMBER,
    XL_CELL_DATE,
    XL_CELL_BOOLEAN,
    XL_CELL_ERROR,
    XL_CELL_BLANK,  # for use in debugging, gathering stats, etc
) = range(7)


class XLSReader(BaseImporter):

    def __init__(self,f,**kwargs):
        self._sheet_name = kwargs.pop('sheet', None)
        self._on_demand = kwargs.pop('on_demand', True)
        super(XLSReader, self).__init__(f)

    def set_reader(self):
        self._workbook = xlrd.open_workbook(self._source.name, on_demand=self._on_demand)
        if self._sheet_name:
            self._reader = self._workbook.sheet_by_name(self._sheet_name)
        else:
            self._reader = self._workbook.sheet_by_index(0)

        self.nrows = self._reader.nrows
        self.ncols = self._reader.ncols

    @property
    def headers(self):
        if not self._headers:
            self._headers = map(self.normalize_string, [self._reader.cell(0, c).value for c in range(self.ncols)])
        return self._headers

    def get_value(self, item, **kwargs):
        """
        Handle different value types for XLS. Item is a cell object.
        """

        # Thx to Augusto C Men to point fast solution for XLS/XLSX dates
        if item.ctype == XL_CELL_DATE:
            return datetime.datetime(*xlrd.xldate_as_tuple(item.value, self._workbook.datemode))

        if item.ctype == XL_CELL_NUMBER:
            if item.value % 1 == 0:  # integers
                return int(item.value)
            else:
                return item.value

        return item.value

    def get_items(self):
        for r in range(1, self.nrows):
            values = [self.get_value(self._reader.cell(r, c)) for c in range(self.ncols)]
            if not any(values):
                continue  # empty lines are ignored
            yield self.get_item(values)


class XLSXReader(XLSReader):

    def set_reader(self):
        self._workbook = openpyxl.reader.excel.load_workbook(self._source)
        if self._sheet_name:
            self._reader = self._workbook.worksheets[self._workbook.get_sheet_names().index(self._sheet_name)]
        else:
            self._reader = self._workbook.worksheets[0]

    @property
    def headers(self):
        if not self._headers:
            self._headers = map(self.normalize_string, [c.value for c in self._reader.rows[0]])
        return self._headers

    def get_value(self, item, **kwargs):
        """
        Handle different value types for XLSX. Item is a cell object.
        """
        # Thx to Augusto C Men to point fast solution for XLS/XLSX dates
        if item.is_date() and isinstance(item, (int, float)):
            return datetime.date(1899, 12, 30) + datetime.timedelta(days=item)
        if item.value is None:
            if item.data_type == item.TYPE_STRING:
                return ''
        return item.value

    def get_items(self):
        for row in self._reader.rows[1:]:
            values = [self.get_value(c) for c in list(row)]
            if not any(values):
                continue  # empty lines are ignored
            yield self.get_item(values)
