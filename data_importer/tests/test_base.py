#/usr/bin/python
# encoding: utf-8
from django.test import TestCase
from ..base import BaseImporter
from cStringIO import StringIO

source_content = StringIO("header1,header2\ntest1,1\ntest2,2\ntest3,3\ntest4,4")


class TestBaseImportMeta(TestCase):

    def setUp(self):
        class TestMeta(BaseImporter):
            fields = [
                'test_field',
                'test2_field',
                'test3_field',
            ]
            class Meta:
                exclude = ['test2_field', 'test3_field']

        self.importer = TestMeta(source=None)

    def test_meta_values(self):
        self.assertEqual(self.importer.Meta.get('exclude'), ['test2_field', 'test3_field'])

    def test_meta_class_values(self):
        self.assertEqual(self.importer.Meta.exclude, ['test2_field', 'test3_field'])

    def test_meta_silent_attributeerror_values(self):
        self.assertFalse(self.importer.Meta.test)

    def test_fields(self):
        self.assertEquals(list(self.importer.fields), ['test_field', ])


class TestReadContent(TestCase):

    def setUp(self):
        class TestMeta(BaseImporter):
                fields = [
                    'test_field',
                    'test2_field',
                    'test3_field',
                ]

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

    def test_read_content_first_line(self):
        self.assertEquals(self.importer.cleaned_data[0],
                          (0, {'test2_field': 'header2', 'test_field': 'HEADER1'}),
                          self.importer.cleaned_data[0])

    def test_read_content_skip_first_line(self):
        class TestMeta(BaseImporter):
                fields = [
                    'test_field',
                    'test_number_field',
                    'test3_field',
                ]

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
                          (0, {'test_number_field': '1', 'test_field': 'TEST1'}),
                          importer.cleaned_data[0])
