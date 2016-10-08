# encoding: utf-8
from __future__ import unicode_literals
from data_importer import models
from django.test import TestCase
import mock
from datetime import date
from imp import reload


def fake_uuid4():
    return 'fake_uuid4'


class TestDataImporterModels(TestCase):

    @mock.patch('uuid.uuid4', fake_uuid4)
    def test_get_random_filename_without_owner(self):
        try:
            reload(models)
        except RuntimeError:
            return True

        instance = models.FileHistory()
        filename = 'test_file.xls'
        today = date.today().strftime("%Y/%m/%d")
        rand_filename = models.get_random_filename(instance, filename)

        expected_name = 'upload_history/anonymous/%s/fake_uuid4.xls' % today
        self.assertEqual(rand_filename, expected_name)
