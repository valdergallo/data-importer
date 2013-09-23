#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from django.test import TestCase
from ..importers.descriptor import ReadDescriptor, InvalidDescriptor, InvalidModel

BASEDIR = os.path.dirname(__file__)
JSON_FILE = os.path.abspath(os.path.join(BASEDIR, '../tests/data/test_json_descriptor.json'))


class ReadDescriptorTestCase(TestCase):

    def setUp(self):
        self.descriptor = ReadDescriptor(file_name=JSON_FILE, model_name='Contact')

    def test_readed_file(self):
        self.assertTrue(self.descriptor.source)

    def test_get_fields(self):
        self.assertEquals(self.descriptor.get_fields(), ["name","year","last"])

    def test_invalid_model(self):
        descriptor = ReadDescriptor(file_name=JSON_FILE, model_name='TestInvalidModel')

        with self.assertRaises(InvalidModel) as error:
            descriptor.get_model()

        self.assertEqual(unicode(error.exception), "Model Name does not exist in descriptor")

    def test_invalid_file(self):
        with self.assertRaises(InvalidDescriptor) as error:
            descriptor = ReadDescriptor(file_name='invalid_file.er', model_name='TestInvalidModel')

        self.assertEqual(unicode(error.exception), "Invalid JSON File Source")

