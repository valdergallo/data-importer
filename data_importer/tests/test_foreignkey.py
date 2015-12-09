#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.test import TestCase
from data_importer.importers import CSVImporter
from data_importer.models_test import ItemInvoice


LOCAL_DIR = os.path.dirname(__file__)


person_content = """invoice,name\n1,test_last_name_1\n2,test_last_name_2\n3,test_last_name_3"""


class TestForeignKeyWithModel(TestCase):
    def setUp(self):
        class TestMeta(CSVImporter):
            class Meta:
                model = ItemInvoice
                delimiter = ','
                raise_errors = False
                ignore_first_line = True

        self.importer = TestMeta(source=person_content.split('\n'))

    def test_get_fields_from_model(self):
        self.assertEquals(self.importer.fields, ['invoice', 'name'])

    def test_values_is_valid(self):
        self.assertFalse(self.importer.is_valid())
