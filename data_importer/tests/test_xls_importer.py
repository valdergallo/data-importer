#!/usr/bin/python
# encoding: utf-8
from django.test import TestCase
from .. import XLSImporter
import os
import datetime
from django.db import models

LOCAL_DIR = os.path.dirname(__file__)


class TestXLSImportMeta(TestCase):

    def setUp(self):
        class TestMeta(XLSImporter):
            fields = [
                'business_place',
                'doc_number',
                'doc_data',
            ]

            class Meta:
                ignore_first_line = True

        self.xls_file = os.path.join(LOCAL_DIR, 'data/test.xls')
        self.importer = TestMeta(source=self.xls_file)

    def test_file_path(self):
        self.assertTrue(os.path.exists(self.xls_file))

    def test_values_is_valid(self):
        self.assertTrue(self.importer.is_valid())

    def test_count_rows(self):
        self.assertEqual(len(self.importer.cleaned_data), 9)

    def test_cleaned_data_content(self):
        content = {
            'doc_number': 10000000,
            'business_place': u'SP',
            'doc_data': datetime.datetime(1982, 11, 1, 0, 0)
            }

        self.assertEquals(self.importer.cleaned_data[0], (0, content),
                          self.importer.cleaned_data)



class Invoice(models.Model):
    business_place = models.CharField(max_length=2)
    doc_number = models.IntegerField()
    doc_data = models.DateTimeField(max_length=10)

    def save(self, *args, **kwargs):
        return self.full_clean() == None


class TestModelXLSImporter(TestCase):

    def setUp(self):
        class TestMeta(XLSImporter):
            class Meta:
                ignore_first_line = True
                model = Invoice

        self.xls_file = os.path.join(LOCAL_DIR, 'data/test.xls')
        self.importer = TestMeta(source=self.xls_file)

    def test_values_is_valid(self):
        self.assertTrue(self.importer.is_valid())

    def test_count_rows(self):
        self.assertEqual(len(self.importer.cleaned_data), 9)

    def test_cleaned_data_content(self):
        content = {
            'doc_number': 10000000,
            'business_place': u'SP',
            'doc_data': datetime.datetime(1982, 11, 1, 0, 0)
            }

        self.assertEquals(self.importer.cleaned_data[0], (0, content),
                          self.importer.cleaned_data)

    def test_save_data(self):
        for row, data in self.importer.cleaned_data:
            instace = Invoice(**data)
            self.assertTrue(instace.save())
