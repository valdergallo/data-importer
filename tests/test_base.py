# encoding: utf-8
from __future__ import unicode_literals
from io import StringIO
from data_importer.importers import BaseImporter
from data_importer.importers import CSVImporter
from data_importer.importers.base import objclass2dict
from data_importer.importers.base import convert_alphabet_to_number
from data_importer.importers.base import reduce_list
from django.test import TestCase
from unittest import skipIf
import data_importer
import django

source_content = StringIO("header1,header2\ntest1,1\ntest2,2\ntest3,3\ntest4,4")


class TestBaseImportMeta(TestCase):

    def setUp(self):
        class MyCSVImporter(CSVImporter):
            fields = [
                'test_field',
                'test2_field',
                'test3_field',
            ]

            class Meta:
                exclude = ['test2_field', 'test3_field']

        self.importer = MyCSVImporter(source=None)

    def test_meta_values(self):
        self.assertEqual(self.importer.Meta.get('exclude'), ['test2_field', 'test3_field'])

    def test_get_author(self):
        self.assertEqual(data_importer.__author__, 'Valder Gallo <valdergallo@gmail.com>')

    def test_get_doc(self):
        self.assertEqual(data_importer.__doc__, 'Data Importer')

    def test_get_meta_higher_doc(self):
        self.assertEqual(BaseImporter.Meta.__doc__, 'Importer configurations')

    def test_get_meta_lower_doc(self):
        self.assertEqual(BaseImporter.meta.__doc__, 'Is same to use .Meta')

    def test_raise_error_in_process_row(self):
        row = ['test1', 'test2', 'test3']
        values = ['test1', 'test2', 'test3', 'test3', 'test3', 'test3']
        base = BaseImporter()
        base.fields = []
        self.assertRaises(TypeError, base.process_row(row, values), 'Invalid Line: 2')

    def test_ignore_empty_lines(self):
        base = BaseImporter()
        row = ['test1', 'test2', 'test3']
        values = [False, False, False]
        base.fields = row
        base.Meta.ignore_empty_lines = True

        self.assertFalse(base.process_row(row, values))

    def test_private_values(self):
        base = CSVImporter()

        self.assertFalse(base._error)
        self.assertFalse(base._cleaned_data)
        self.assertFalse(base._fields)
        self.assertFalse(base._reader)
        self.assertFalse(base._excluded)
        self.assertFalse(base._readed)

    def test_meta_class_values(self):
        self.assertEqual(self.importer.Meta.exclude, ['test2_field', 'test3_field'])

    def test_meta_silent_attributeerror_values(self):
        self.assertFalse(self.importer.Meta.test)

    def test_fields(self):
        self.assertEqual(list(self.importer.fields), ['test_field', ])

    def test_objclass2dict(self):
        class Meta:
            test_1 = 1
            test_2 = 2
            test_3 = 3

        return_dict = objclass2dict(Meta)
        self.assertEqual(return_dict, {'test_1': 1, 'test_2': 2, 'test_3': 3})


class ImportersTests(TestCase):
    def test_xls_importers(self):
        import data_importer
        self.assertTrue(data_importer.importers.XLSImporter)

    def test_xlsx_importers(self):
        import data_importer
        self.assertTrue(data_importer.importers.XLSXImporter)

    def test_base_importers(self):
        import data_importer
        self.assertTrue(data_importer.importers.XMLImporter)


class TestClassObjToLazyDict(TestCase):

    def setUp(self):
        from data_importer.importers.base import objclass2dict

        class MyTestClass:
            test_field = 'test'

        self.testclass = objclass2dict(MyTestClass)

    def test_get_object(self):
        self.assertTrue(self.testclass.test_field)

    def test_get_false_without_raises(self):
        self.assertFalse(self.testclass.not_raise_error)


class TestReadContent(TestCase):

    def setUp(self):
        class MyCSVImporter(CSVImporter):
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
        self.importer = MyCSVImporter(source=self.source_content)

    def test_read_content(self):
        self.assertTrue(self.importer.is_valid(), self.importer.errors)

    def test_meta_lower(self):
        self.assertEqual(self.importer.meta.delimiter, ',')

    def test_is_valid(self):
        self.assertTrue(self.importer.is_valid())

    def test_read_content_first_line(self):
        self.assertEqual(self.importer.cleaned_data[0],
                          (1, {'test2_field': 'header2', 'test_field': 'HEADER1'}),
                          self.importer.cleaned_data[0])

    def test_errors(self):
        self.assertFalse(self.importer.errors)
        self.assertFalse(self.importer._error)

    def test_start_fields(self):
        self.importer.start_fields()
        self.assertEqual(self.importer.fields, ['test_field', 'test2_field'])

    def test_raise_error_on_clean(self):
        class MyCSVImporterClean(CSVImporter):
            fields = ['test', ]

            def clean_test(self, value):
                value.coisa = 1

        importer_error = MyCSVImporterClean(source=['test1', ])

        self.assertFalse(importer_error.is_valid())
        # test get row
        self.assertEqual(importer_error.errors[0][0], 1)
        # test get error type
        self.assertEqual(importer_error.errors[0][1], 'ValidationError')
        # test get error message
        self.assertIn('object has no attribute coisa', importer_error.errors[0][2])


    def test_read_content_skip_first_line(self):
        class MyCSVImporter(CSVImporter):
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
        importer = MyCSVImporter(source=self.source_content)
        self.assertTrue(importer.is_valid(), importer.errors)
        self.assertEqual(importer.cleaned_data[0],
                          (1, {'test_number_field': '1', 'test_field': 'TEST1'}),
                          importer.cleaned_data[0])

    def test_exclude_with_tupla(self):
        class MyCSVImporter(CSVImporter):
                fields = [
                    'test_field',
                    'test_number_field',
                    'test3_field',
                ]

                class Meta:
                    exclude = ('test3_field',)
                    delimiter = ','
                    raise_errors = True
                    ignore_first_line = True

                def clean_test_field(self, value):
                    return str(value).upper()

        self.source_content.seek(0)
        importer = MyCSVImporter(source=self.source_content)
        self.assertTrue(importer.is_valid(), importer.errors)
        self.assertEqual(importer.cleaned_data[0],
                          (1, {'test_number_field': '1', 'test_field': 'TEST1'}),
                          importer.cleaned_data[0])


class MyBaseImporter(BaseImporter):
    fields = ('name', 'value')

    class Meta:
        delimiter = ','


class BaseImporterTest(TestCase):

    @skipIf(django.VERSION < (1, 4), "not supported in this library version")
    def test_raise_not_implemented(self):
        with self.assertRaisesMessage(NotImplementedError, "No reader implemented"):
            instance = MyBaseImporter(source=source_content)
            instance.set_reader()


class TestConvertLetterToNumber(TestCase):

    def test_convert_text_lower_to_number(self):
        r = convert_alphabet_to_number("a")
        self.assertEqual(r, 0)

    def test_convert_text_upper_to_number(self):
        r = convert_alphabet_to_number("C")
        self.assertEqual(r, 2)

    def test_convert_worlds_to_number(self):
        r = convert_alphabet_to_number("ACDC")
        self.assertEqual(r, 1342)


class TestReduceList(TestCase):

    def test_reduce_list(self):
        list_values = [1,2,3,4,5,6]
        list_key = [1,3,6]
        reduced = reduce_list(list_key, list_values)
        self.assertEqual(reduced, [2, 4])

    def test_reduce_list_two(self):
        list_values = [1,2,3,4,5,6]
        list_key = [0,2,3]
        reduced = reduce_list(list_key, list_values)
        self.assertEqual(reduced, [1, 3, 4])
