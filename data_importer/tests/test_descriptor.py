#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from django.test import TestCase
from ..importers.descriptor import ReadDescriptor

BASEDIR = os.path.dirname(__file__)

class ReadDescriptorTestCase(TestCase):

    def setUp(self):
        json_file = os.path.abspath(os.path.join(BASEDIR, '../tests/data/test_json_descriptor.json'))
        self.descriptor = ReadDescriptor(file_name=json_file, model_name='TestLoad')

    def test_readed_file(self):
        self.assertTrue(self.descriptor.source)

