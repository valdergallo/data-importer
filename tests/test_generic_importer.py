# encoding: utf-8
from __future__ import unicode_literals
import mock
import os
from unittest import TestCase
from unittest import skipIf
from data_importer.importers.generic import GenericImporter
from data_importer.readers.xls_reader import XLSReader
from data_importer.readers.xlsx_reader import XLSXReader
from data_importer.readers.csv_reader import CSVReader
from data_importer.readers.xml_reader import XMLReader
from data_importer.core.exceptions import UnsuportedFile


LOCAL_DIR = os.path.dirname(__file__)


class TestGenericImporterSetup(TestCase):

    def setUp(self):
        self.xls_file = os.path.join(LOCAL_DIR, 'data/test.xls')
        self.xlsx_file = os.path.join(LOCAL_DIR, 'data/test.xlsx')
        self.csv_file = os.path.join(LOCAL_DIR, 'data/test.csv')
        self.xml_file = os.path.join(LOCAL_DIR, 'data/test.xml')
        self.unsuported_file = os.path.join(LOCAL_DIR, 'data/test_json_descriptor.json')

    def test_xls_reader_set(self):
        importer = GenericImporter(source=self.xls_file)
        self.assertEquals(importer.get_reader_class(), XLSReader)

    def test_xlsx_reader_set(self):
        importer = GenericImporter(source=self.xlsx_file)
        self.assertEquals(importer.get_reader_class(), XLSXReader)

    def test_csv_reader_set(self):
        importer = GenericImporter(source=self.csv_file)
        self.assertEquals(importer.get_reader_class(), CSVReader)

    def test_xml_reader_set(self):
        importer = GenericImporter(source=self.xml_file)
        self.assertEquals(importer.get_reader_class(), XMLReader)

    def test_getting_source_file_extension(self):
        importer = GenericImporter(source=self.csv_file)
        self.assertEquals(importer.get_source_file_extension(), 'csv')

    def test_import_with_file_instance(self):
        file_instance = open(self.csv_file)
        importer = GenericImporter(source=file_instance)
        self.assertEquals(importer.get_source_file_extension(), 'csv')


