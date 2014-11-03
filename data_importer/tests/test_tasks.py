#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from data_importer.tasks import DataImpoterTask


class FakeFileInstance(object):
    filename = 'fake_filename.csv'


class DataImporterTaskTest(TestCase):

    def setUp(self):
        self.task = DataImpoterTask()
