#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.conf import settings
import data_importer


class SettingsDataImporterContentTest(TestCase):

    def test_data_importer_excel_decoder(self):
        self.assertEqual(data_importer.importers.base.DATA_IMPORTER_EXCEL_DECODER, 'cp1252')

    def test_data_importer_decoder(self):
        self.assertEqual(data_importer.importers.base.DATA_IMPORTER_DECODER, 'utf-8')

