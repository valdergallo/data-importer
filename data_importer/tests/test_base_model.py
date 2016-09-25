# encoding: utf-8
from __future__ import unicode_literals
from django.test import TestCase
from data_importer.importers import CSVImporter
import os
from django.core.files import File as DjangoFile
from example.models import Person
from example.models import Mercado
from example.models import PersonFile
from example.models import Invoice
from distutils.version import StrictVersion
import django
from io import IOBase
from io import BufferedReader
from io import TextIOWrapper


LOCAL_DIR = os.path.dirname(__file__)


person_content = """first_name,last_name,age\ntest_first_name_1,test_last_name_1,age1\ntest_first_name_2,test_last_name_2,age2\ntest_first_name_3,test_last_name_3,age3"""


class TestBaseWithModel(TestCase):
    def setUp(self):
        class TestMeta(CSVImporter):
            class Meta:
                model = Person
                delimiter = ','
                raise_errors = True
                ignore_first_line = True

        self.importer = TestMeta(source=person_content.split('\n'))

    def test_get_fields_from_model(self):
        self.assertEquals(self.importer.fields, ['first_name', 'last_name', 'age'])

    def test_values_is_valid(self):
        self.assertTrue(self.importer.is_valid())

    def test_cleaned_data_content(self):
        content = {'first_name': 'test_first_name_1',
                   'last_name': 'test_last_name_1',
                   'age': 'age1'}
        self.assertEquals(self.importer.cleaned_data[0], (1, content))

    def test_source_importer_file(self):
        base = CSVImporter(source=open('test.txt', 'w'))
        self.assertEqual(type(base._source), TextIOWrapper, type(base._source))

    def test_source_importer_list(self):
        base = CSVImporter(source=['test1', 'test2'])
        self.assertEqual(type(base._source), list, type(base._source))

    def test_source_importer_django_file(self):
        person = PersonFile()
        person.filefield = DjangoFile(open('test.txt', 'w'))

        base = CSVImporter(source=person.filefield)
        self.assertEqual(type(base._source), BufferedReader, type(base._source))

    def test_save_data_content(self):
        for row, data in self.importer.cleaned_data:
            instace = Person(**data)
            instace.save()
            self.assertTrue(instace.id)

    def tearDown(self):
        try:
            os.remove('test.txt')
        except:
            pass


class TestPTBRCSVImporter(TestCase):

    def setUp(self):
        class TestMeta(CSVImporter):
            class Meta:
                ignore_first_line = True
                delimiter = ';'
                model = Mercado

        self.csv_file = os.path.join(LOCAL_DIR, 'data/ptbr_test_win.csv')
        self.importer = TestMeta(source=self.csv_file)

    def test_values_is_valid(self):
        self.assertTrue(self.importer.is_valid())

    def test_count_rows(self):
        self.assertEqual(len(self.importer.cleaned_data), 4)

    def test_cleaned_data_content(self):
        content = {
            'item': 'Caça',
            'qtde': '1',
            }

        self.assertEquals(self.importer.cleaned_data[0], (1, content),
                          self.importer.cleaned_data[0])

        content = {
            'item': 'Amanhã',
            'qtde': '2',
            }

        self.assertEquals(self.importer.cleaned_data[1], (2, content),
                          self.importer.cleaned_data)

        content = {
            'item': 'Qüanto',
            'qtde': '3',
            }

        self.assertEquals(self.importer.cleaned_data[2], (3, content),
                          self.importer.cleaned_data)

        content = {
            'item': 'Será',
            'qtde': '4',
            }

        self.assertEquals(self.importer.cleaned_data[3], (4, content),
                          self.importer.cleaned_data)


class TestModelValidator(TestCase):

    def setUp(self):
        class TestMeta(CSVImporter):
            class Meta:
                ignore_first_line = True
                delimiter = ';'
                model = Invoice

        self.csv_file = os.path.join(LOCAL_DIR, 'data/invoice.csv')
        self.importer = TestMeta(source=self.csv_file)

    def test_values_is_valid(self):
        self.assertFalse(self.importer.is_valid())

    def test_errors_values(self):
        self.importer.is_valid()
        DJANGO_VERSION = StrictVersion(django.get_version())
        if DJANGO_VERSION < StrictVersion('1.4'):
            error = [(1, 'ValidationError', 'Field (price) This value must be a float.')]
        else:
            error = [(1, 'ValidationError', 'Field (price) 23,98 value must be a float.')]

        self.assertEquals(self.importer.errors, error, self.importer.cleaned_data)
