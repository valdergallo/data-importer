#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from data_importer.tasks import DataImpoterTask


class FakeFileInstance(object):
    filename = 'fake_filename.csv'


class DataImporterTaskTest(TestCase):

    def setUp(self):
        self.task = DataImpoterTask()

    def test_get_mimetype(self):
        mimetype = self.task.get_mimetype(FakeFileInstance)
        self.assertEqual(mimetype, 'csv')

    def test_get_parser(self):
        self.task.get_mimetype(FakeFileInstance)
        parser_name = self.task.get_parser()
        self.assertEqual(parser_name.__name__, 'parse_csv')
