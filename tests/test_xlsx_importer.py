# encoding: utf-8
from __future__ import unicode_literals
from django.test import TestCase
from data_importer.importers.xlsx_importer import XLSXImporter
import os
import datetime
from django.db import models

LOCAL_DIR = os.path.dirname(__file__)


class TestXLSImportMeta(TestCase):

    def setUp(self):
        class TestMeta(XLSXImporter):
            fields = [
                'business_place',
                'doc_number',
                'doc_data',
            ]

            class Meta:
                ignore_first_line = True

        self.xls_file = os.path.join(LOCAL_DIR, 'data/test.xlsx')
        self.importer = TestMeta(source=self.xls_file)

    def test_file_path(self):
        self.assertTrue(os.path.exists(self.xls_file))

    def test_values_is_valid(self):
        self.assertTrue(self.importer.is_valid())

    def test_count_rows(self):
        self.assertEqual(len(self.importer.cleaned_data), 9)

    def test_cleaned_data_content(self):
        content = {'doc_number': 1000000, 'business_place': 'SP',
        'doc_data': datetime.datetime(1982, 11, 1, 0, 0)}

        self.assertEqual(self.importer.cleaned_data[0], (1, content),
                          self.importer.cleaned_data)



class InvoiceXLSX(models.Model):
    business_place = models.CharField(max_length=2)
    doc_number = models.IntegerField()
    doc_data = models.DateTimeField(max_length=10)

    def save(self, *args, **kwargs):
        return self.full_clean() == None


class TestModelXLSImporter(TestCase):

    def setUp(self):
        class TestMeta(XLSXImporter):
            class Meta:
                ignore_first_line = True
                model = InvoiceXLSX

        self.xls_file = os.path.join(LOCAL_DIR, 'data/test.xlsx')
        self.importer = TestMeta(source=self.xls_file)

    def test_values_is_valid(self):
        self.assertTrue(self.importer.is_valid())

    def test_count_rows(self):
        self.assertEqual(len(self.importer.cleaned_data), 9)

    def test_cleaned_data_content(self):
        content = {'doc_number': 1000000, 'business_place': 'SP',
        'doc_data': datetime.datetime(1982, 11, 1, 0, 0)}

        self.assertEqual(self.importer.cleaned_data[0], (1, content),
                          self.importer.cleaned_data)

    def test_save_data(self):
        for row, data in self.importer.cleaned_data:
            instace = InvoiceXLSX(**data)
            self.assertTrue(instace.save())

    def test_save_importer(self):
        self.assertTrue(self.importer.save())


class MercadoXLSX(models.Model):
    item = models.CharField(max_length=50)
    qtde = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        return self.full_clean() == None


class TestPTBRXLSImporter(TestCase):

    def setUp(self):
        class TestMeta(XLSXImporter):
            class Meta:
                ignore_first_line = True
                model = MercadoXLSX

        self.xls_file = os.path.join(LOCAL_DIR, 'data/ptbr_test.xlsx')
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

        self.assertEqual(self.importer.cleaned_data[0], (1, content),
                          self.importer.cleaned_data)

        content = {
            'item': 'Amanhã',
            'qtde': 2,
            }

        self.assertEqual(self.importer.cleaned_data[1], (2, content),
                          self.importer.cleaned_data)

        content = {
            'item': 'Qüanto',
            'qtde': 3,
            }

        self.assertEqual(self.importer.cleaned_data[2], (3, content),
                          self.importer.cleaned_data)

        content = {
            'item': 'Será',
            'qtde': 4,
            }

        self.assertEqual(self.importer.cleaned_data[3], (4, content),
                          self.importer.cleaned_data)

