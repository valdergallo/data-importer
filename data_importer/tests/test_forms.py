# -*- coding: utf-8 -*-
from django.test import TestCase
from cStringIO import StringIO
from mock import Mock
import sys
from data_importer import forms

source_content = StringIO("header1,header2\ntest1,1\ntest2,2\ntest3,3\ntest4,4")


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
