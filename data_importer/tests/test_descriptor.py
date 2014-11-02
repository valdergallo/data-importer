#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from django.test import TestCase
from data_importer.importers.descriptor import ReadDescriptor
from data_importer.importers.descriptor import InvalidDescriptor
from data_importer.importers.descriptor import InvalidModel

BASEDIR = os.path.dirname(__file__)
JSON_FILE = os.path.abspath(os.path.join(BASEDIR, '../tests/data/test_json_descriptor.json'))


class ReadDescriptorTestCase(TestCase):

    def setUp(self):
        self.descriptor = ReadDescriptor(file_name=JSON_FILE, model_name='Contact')

    def test_readed_file(self):
        self.assertTrue(self.descriptor.source)

    def test_get_fields(self):
        self.assertEquals(self.descriptor.get_fields(), ["name", "year", "last"])

    def test_invalid_model(self):
        descriptor = ReadDescriptor(file_name=JSON_FILE, model_name='TestInvalidModel')
        self.assertRaises(InvalidModel, lambda: descriptor.get_model())

    def test_invalid_file(self):
        self.assertRaises(InvalidDescriptor, lambda: ReadDescriptor(file_name='invalid_file.er',
                          model_name='TestInvalidModel'))
