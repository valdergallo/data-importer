# encoding: utf-8
from __future__ import unicode_literals
from unittest import TestCase
from data_importer.importers.xls_importer import XLSImporter
import os
import datetime

LOCAL_DIR = os.path.dirname(__file__)


class TestModelXLSImporter(TestCase):
    def setUp(self):
        class TestMeta(XLSImporter):
            fields = ["business_place", "doc_number", "doc_data"]
            class Meta:
                ignore_first_line = True

        self.xls_file = os.path.join(LOCAL_DIR, 'data/test.xls')
        self.importer = TestMeta(source=self.xls_file)

        class TestMetaDict(XLSImporter):
            fields = ["business_place", "doc_number", "doc_data"]
            class Meta:
                ignore_first_line = True

        self.importer_dict = TestMetaDict(source=self.xls_file)

    def test_values_is_valid(self):
        self.assertTrue(self.importer.is_valid())
        self.assertTrue(self.importer_dict.is_valid())

    def test_count_rows(self):
        self.assertEqual(len(self.importer.cleaned_data), 9)
        self.assertEqual(len(self.importer_dict.cleaned_data), 9)

    def test_cleaned_data_content(self):
        content = {
            'doc_number': 10000000,
            'business_place': 'SP',
            'doc_data': datetime.datetime(1982, 11, 1, 0, 0)
        }

        self.assertEquals(self.importer.cleaned_data[0], (1, content), self.importer.cleaned_data)
        self.assertEquals(self.importer_dict.cleaned_data[0], (1, content), self.importer_dict.cleaned_data)


class TestPTBRXLSImporter(TestCase):
    def setUp(self):
        class TestMeta(XLSImporter):
            fields = ["item", "qtde"]
            class Meta:
                ignore_first_line = True

        self.xls_file = os.path.join(LOCAL_DIR, 'data/ptbr_test.xls')
        self.importer = TestMeta(source=self.xls_file)

    def test_values_is_valid(self):
        self.assertTrue(self.importer.is_valid())

    def test_count_rows(self):
        self.assertEqual(len(self.importer.cleaned_data), 4)

    def test_cleaned_data_content(self):
        content = {
            'item': 'Caça',
            'qtde': 1,
        }

        self.assertEquals(self.importer.cleaned_data[0], (1, content),
                          self.importer.cleaned_data)

        content = {
            'item': 'Amanhã',
            'qtde': 2,
        }

        self.assertEquals(self.importer.cleaned_data[1], (2, content),
                          self.importer.cleaned_data)

        content = {
            'item': 'Qüanto',
            'qtde': 3,
        }

        self.assertEquals(self.importer.cleaned_data[2], (3, content),
                          self.importer.cleaned_data)

        content = {
            'item': 'Será',
            'qtde': 4,
        }

        self.assertEquals(self.importer.cleaned_data[3], (4, content),
                          self.importer.cleaned_data)
