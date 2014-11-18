#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from data_importer.importers.general import DefaultImporter
from data_importer.readers.xls_reader import XLSReader
from data_importer.readers.xlsx_reader import XLSXReader
from data_importer.readers.csv_reader import CSVReader
import os

LOCAL_DIR = os.path.dirname(__file__)


class TestGeneralImpoerterSetup(TestCase):

    def setUp(self):
        self.xls_file = os.path.join(LOCAL_DIR, 'data/test.xls')
        self.xlsx_file = os.path.join(LOCAL_DIR, 'data/test.xlsx')
        self.csv_file = os.path.join(LOCAL_DIR, 'data/test.csv')

    def test_xls_reader_set(self):
        importer = DefaultImporter(source=self.xls_file)
        self.assertEquals(importer.get_reader_class(), XLSReader)

    def test_xlsx_reader_set(self):
        importer = DefaultImporter(source=self.xlsx_file)
        self.assertEquals(importer.get_reader_class(), XLSXReader)

    def test_csv_reader_set(self):
        importer = DefaultImporter(source=self.csv_file)
        self.assertEquals(importer.get_reader_class(), CSVReader)

    def test_getting_source_file_extension(self):
        importer = DefaultImporter(source=self.csv_file)
        self.assertEquals(importer.get_source_file_extension(), 'csv')
