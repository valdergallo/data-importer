# -*- coding: utf-8 -*-
from django.test import TestCase
from mock import Mock
import sys
from data_importer import forms
from imp import reload


class TestFileUploadForm(TestCase):

    def setUp(self):
        self.form = forms.FileUploadForm()

    def test_invalid_form(self):
        self.assertFalse(self.form.is_valid())

    def test_default_importer(self):
        self.assertEqual(self.form.importer, None)

    def test_default_importer_task(self):
        self.assertEqual(self.form.is_task, True)


class TestTaskImporter(TestCase):

    def test_celery_importer(self):
        sys.modules['celery'] = Mock()
        reload(forms)
        self.assertEqual(forms.HAS_CELERY, True)
