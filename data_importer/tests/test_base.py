#/usr/bin/python
# encoding: utf-8
from django.test import TestCase
from ..base import BaseImporter
from cStringIO import StringIO
from django.db import models

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

        self.FirstTest = TestMeta(source=None)

    def test_meta_values(self):
        self.assertEqual(self.FirstTest.Meta.get('exclude'), ['test2_field', 'test3_field'])

    def test_meta_class_values(self):
        self.assertEqual(self.FirstTest.Meta.exclude, ['test2_field', 'test3_field'])

    def test_meta_silent_attributeerror_values(self):
        self.assertFalse(self.FirstTest.Meta.test)

    def test_fields(self):
        self.assertEquals(list(self.FirstTest.fields), ['test_field', ])


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

        self.TestMeta = TestMeta

        self.source_content = source_content
        self.source_content.seek(0)
        self.FirstTest = TestMeta(source=self.source_content)

    def test_read_content(self):
        self.assertTrue(self.FirstTest.is_valid(), self.FirstTest.errors)

    def test_read_content_first_line(self):
        self.assertEquals(self.FirstTest.cleaned_data[0],
                          (0, {'test2_field': 'header2', 'test_field': 'HEADER1'}),
                          self.FirstTest.cleaned_data[0])

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
        FirstTest = TestMeta(source=self.source_content)
        self.assertTrue(FirstTest.is_valid(), FirstTest.errors)
        self.assertEquals(FirstTest.cleaned_data[0],
                          (0, {'test_number_field': '1', 'test_field': 'TEST1'}),
                          FirstTest.cleaned_data[0])


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.CharField(max_length=10)


person_content = StringIO("first_name,last_name,age\ntest_first_name_1,test_last_name_1,age1\ntest_first_name_2,test_last_name_2,age2\ntest_first_name_3,test_last_name_3,age3")


class TestBaseWithModel(TestCase):
    def setUp(self):
        class TestMeta(BaseImporter):
            class Meta:
                model = Person
                delimiter = ','
                raise_errors = True
                ignore_first_line = True

        self.ModelTest = TestMeta(source=person_content)

    def test_get_fields_from_model(self):
        self.assertEquals(self.ModelTest.fields, ['age', 'first_name', 'last_name'])

    def test_values_is_valid(self):
        self.assertTrue(self.ModelTest.is_valid())

    def test_cleaned_data_content(self):
        self.assertEquals(self.ModelTest.cleaned_data[0], (0, {'age': 'test_first_name_1', 'last_name': 'age1', 'first_name': 'test_last_name_1'}), self.ModelTest.cleaned_data)

    def test_save_data(self):
        for row, data in self.ModelTest.cleaned_data:
            instace = Person(**data)
            self.assertTrue(instace.save())
