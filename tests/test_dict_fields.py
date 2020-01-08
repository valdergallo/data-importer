# encoding: utf-8
from __future__ import unicode_literals
from io import StringIO
from data_importer.importers import CSVImporter
from django.test import TestCase
from collections import OrderedDict


source_content = StringIO("header1,header2,header3\ntest1,1,exclude1\ntest2,2,exclude2\ntest3,3,exclude3\ntest4,4,exclude4")

class TestReadContent(TestCase):

    def setUp(self):
        class TestMeta(CSVImporter):
            fields = OrderedDict((
                ('test_field', 0),
                ('test2_field', 1),
                ('test3_field', 2),
            ))

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
        self.assertEqual(self.importer.cleaned_data[0],
                          (1, OrderedDict({'test_field': 'HEADER1', 'test2_field': 'header2'})))

    def test_errors(self):
        self.assertFalse(self.importer.errors)
        self.assertFalse(self.importer._error)

    def test_start_fields(self):
        self.importer.start_fields()
        self.assertEqual(self.importer.fields, ['test_field', 'test2_field'])

    def test_raise_error_on_clean(self):
        class TestMetaClean(CSVImporter):
            fields = ['test', ]

            def clean_test(self, value):
                value.coisa = 1

        importer_error = TestMetaClean(source=['test1', ])

        self.assertFalse(importer_error.is_valid())
        # test get row
        self.assertEqual(importer_error.errors[0][0], 1)
        # test get error type
        self.assertEqual(importer_error.errors[0][1], 'ValidationError')
        # test get error message
        self.assertIn('object has no attribute coisa', importer_error.errors[0][2])

    def test_read_content_skip_first_line(self):
        class TestMeta(CSVImporter):
                fields = OrderedDict((
                    ('test_field', 'A'),
                    ('test_number_field', 'B'),
                    ('test3_field', 'c'),
                ))

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
        should_be = (1, OrderedDict([('test_field', 'TEST1'), ('test_number_field', '1')]))
        self.assertEqual(importer.cleaned_data[0],
                          should_be)

    def test_exclude_with_tupla(self):
        class TestMeta(CSVImporter):
                fields = OrderedDict((
                    ('test_field', 0),
                    ('test_number_field', 'b'),
                    ('test3_field', 'c'),
                ))

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
        should_be = (1, OrderedDict([('test_field', 'TEST1'), ('test_number_field', '1')]))
        self.assertEqual(importer.cleaned_data[0],
                          should_be)
