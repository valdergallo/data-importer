#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cStringIO import StringIO
from data_importer.importers import CSVImporter
from django.test import TestCase

source_content = StringIO("header1,header2\ntest1,1\ntest2,2\ntest3,3\ntest4,4")


class TestReadContent(TestCase):

    def setUp(self):
        class TestMeta(CSVImporter):
                fields = {
                    'test_field': 1,
                    'test2_field': 2,
                    'test3_field': 3,
                }

                class Meta:
                    exclude = ['test3_field']
                    delimiter = ','
                    raise_errors = True

                def clean_test_field(self, value):
                    return str(value).upper()

        self.source_content = source_content
        self.source_content.seek(0)
        self.importer = TestMeta(source=self.source_content)

    def test_read_content(self):
        self.assertTrue(self.importer.is_valid(), self.importer.errors)

    def test_meta_lower(self):
        self.assertEqual(self.importer.meta.delimiter, ',')

    def test_is_valid(self):
        self.assertTrue(self.importer.is_valid())

    def test_read_content_first_line(self):
        self.assertEquals(self.importer.cleaned_data[0],
                          (1, {'test2_field': 'header2', 'test_field': 'HEADER1'}),
                          self.importer.cleaned_data[0])

    def test_errors(self):
        self.assertFalse(self.importer.errors)
        self.assertFalse(self.importer._error)

    def test_start_fields(self):
        self.importer.start_fields()
        self.assertEquals(self.importer.fields, ['test_field', 'test2_field'])

    def test_raise_error_on_clean(self):
        class TestMetaClean(CSVImporter):
            fields = ['test', ]

            def clean_test(self, value):
                value.coisa = 1

        importer_error = TestMetaClean(source=['test1', ])

        self.assertFalse(importer_error.is_valid())
        self.assertEqual(importer_error.errors, [(1, 'AttributeError',
                         u"unicode object has no attribute coisa")])

    def test_read_content_skip_first_line(self):
        class TestMeta(CSVImporter):
                fields = {
                    'test_field': 'A',
                    'test_number_field': 'B',
                    'test3_field': 'c',
                }

                class Meta:
                    exclude = ['test3_field']
                    delimiter = ','
                    raise_errors = True
                    ignore_first_line = True

                def clean_test_field(self, value):
                    return str(value).upper()

        self.source_content.seek(0)
        importer = TestMeta(source=self.source_content)
        self.assertTrue(importer.is_valid(), importer.errors)
        self.assertEquals(importer.cleaned_data[0],
                          (1, {'test_number_field': '1', 'test_field': 'TEST1'}),
                          importer.cleaned_data[0])

    def test_exclude_with_tupla(self):
        class TestMeta(CSVImporter):
                fields = {
                    'test_field': 0,
                    'test_number_field': 'A',
                    'test3_field': 'b',
                }

                class Meta:
                    exclude = ('test3_field',)
                    delimiter = ','
                    raise_errors = True
                    ignore_first_line = True

                def clean_test_field(self, value):
                    return str(value).upper()

        self.source_content.seek(0)
        importer = TestMeta(source=self.source_content)
        self.assertTrue(importer.is_valid(), importer.errors)
        self.assertEquals(importer.cleaned_data[0],
                          (1, {'test_number_field': '1', 'test_field': 'TEST1'}),
                          importer.cleaned_data[0])
