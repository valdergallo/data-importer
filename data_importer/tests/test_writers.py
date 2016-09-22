from __future__ import unicode_literals
from django.test import TestCase
from data_importer.writers.utils import QuerysetToWorkbook
from example.models import Person
from django.core.files import File
from django.http import HttpResponse
from io import BytesIO
import os

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone


def createFivePerson():
    for i in range(1, 5):
        Person.objects.create(first_name='first_name_' + str(i),
                             last_name='last_name_' + str(i),
                             age='1' + str(i))


class TestQuerysetToWorkbook(TestCase):
    pass


class TestSQLToWorkBook(TestCase):
    pass


class TestQuerysetToWorkbookMethods(TestCase):

    def setUp(self):
        createFivePerson()
        queryset = Person.objects.all()
        columns = ['First Name', 'Last Name', 'Age']
        self.instance = QuerysetToWorkbook(queryset, columns, filename='report')

    def tearDown(self):
        if hasattr(self, 'zip_saved_file'):
            os.remove(self.instance.get_filename(extension='zip'))

        if hasattr(self, 'saved_file'):
            os.remove(self.instance.get_filename())

    def test_queryset_to_workbook(self):
        workbook = self.instance.queryset_to_workbook()
        rows = workbook.active.rows[0]
        self.assertEqual(len(rows), 3)

    def test_get_first(self):
        self.instance.queryset_to_workbook()
        first_row = self.instance.get_first()
        self.assertEqual(first_row, 'A1:C1')

    def test_set_colums(self):
        dict_colums = {'test_column': 'Test Column', 'new_test': 'New Test'}
        self.instance.columns = dict_colums.values()
        self.assertEqual(self.instance.columns, dict_colums)

    def test_get_data(self):
        class LazyDict(object):
            test_column = 'Test Column'
            new_test = 'New Test',
            age = 1
            first_name = 'John'
            last_name = 'Constantine'

        data_cleaned = {'age': 1, 'first_name': 'John', 'last_name': 'Constantine'}
        removed = self.instance.get_data(self.instance.columns, LazyDict())
        self.assertEqual(removed, data_cleaned)

    def test_get_filename(self):
        file_name = self.instance.filename + '_' + timezone.now().strftime('%Y%m%d') + '.' + 'xlsx'
        self.assertEqual(self.instance.get_filename(), file_name)

    def test_get_content(self):
        string_io = self.instance.get_content()
        self.assertIsInstance(string_io, BytesIO)

    def test_get_compressed_file(self):
        string_io = self.instance.get_compressed_file()
        self.assertIsInstance(string_io, BytesIO)

    def test_compress_django_file(self):
        django_file = self.instance.compress_django_file()
        self.assertIsInstance(django_file, File)

    def test_save_compress(self):
        self.zip_saved_file = self.instance.save(compress=True)
        self.assertTrue(os.path.exists(self.instance.get_filename(extension='zip')))

    def test_save_file(self):
        self.saved_file = self.instance.save(compress=False)
        self.assertTrue(os.path.exists(self.instance.get_filename()))

    def test_response_compressed(self):
        response = self.instance.response(compress=True)
        self.assertIsInstance(response, HttpResponse)
        self.assertTrue(response['Content-Disposition'])

    def test_response(self):
        response = self.instance.response(compress=False)
        self.assertIsInstance(response, HttpResponse)
        self.assertTrue(response['Content-Disposition'])
