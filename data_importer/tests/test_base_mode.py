#!/usr/bin/python
# encoding: utf-8
from django.test import TestCase
from .. import BaseImporter
from cStringIO import StringIO
from django.db import models


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

        self.importer = TestMeta(source=person_content)

    def test_get_fields_from_model(self):
        self.assertEquals(self.importer.fields, ['first_name', 'last_name', 'age'])

    def test_values_is_valid(self):
        self.assertTrue(self.importer.is_valid())

    def test_cleaned_data_content(self):
        content = {'first_name': 'test_first_name_1',
            'last_name': 'test_last_name_1', 'age': 'age1'}

        self.assertEquals(self.importer.cleaned_data[0], (0, content),
                          self.importer.cleaned_data)

    def test_save_data(self):
        for row, data in self.importer.cleaned_data:
            instace = Person(**data)
            self.assertTrue(instace.save())
