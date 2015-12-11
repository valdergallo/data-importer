#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock
import os
import django
from django.test import TestCase
from unittest import skipIf
from data_importer.importers.generic import GenericImporter
from data_importer.readers.xls_reader import XLSReader
from data_importer.readers.xlsx_reader import XLSXReader
from data_importer.readers.csv_reader import CSVReader
from data_importer.readers.xml_reader import XMLReader
from data_importer.core.exceptions import UnsuportedFile
from data_importer.models import FileHistory
from example.models import Invoice


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

    @skipIf(django.VERSION < (1, 4), "not supported in this library version")
    def test_unsuported_raise_error_message(self):
        with self.assertRaisesMessage(UnsuportedFile, 'Unsuported File'):
            GenericImporter(source=self.unsuported_file)

    def test_import_with_file_instance(self):
        file_instance = open(self.csv_file)
        importer = GenericImporter(source=file_instance)
        self.assertEquals(importer.get_source_file_extension(), 'csv')

    def test_import_with_model_instance(self):
        file_mock = mock.MagicMock(spec=FileHistory, name='FileHistoryMock')
        file_mock.file_upload = '/media/test.csv'

        importer = GenericImporter(source=file_mock)
        self.assertEquals(importer.get_source_file_extension(), 'csv')


class CustomerDataImporter(GenericImporter):
    class Meta:
        model = Invoice
        ignore_first_line = True


class TestGenericImporterBehavior(TestCase):

    def setUp(self):
        self.xls_file = os.path.join(LOCAL_DIR, 'data/test_invalid_lines.xlsx')

    def test_xlsx_is_not_valid(self):
        instance = CustomerDataImporter(source=self.xls_file)
        self.assertFalse(instance.is_valid())

    def test_save_lines_without_errors(self):
        instance = CustomerDataImporter(source=self.xls_file)
        instance.save()

        count_invoices = Invoice.objects.count()
        self.assertEqual(count_invoices, 6, ('error', count_invoices))

    def test_get_three_errors(self):
        instance = CustomerDataImporter(source=self.xls_file)
        instance.is_valid()
        self.assertEqual(len(instance.errors), 3)
