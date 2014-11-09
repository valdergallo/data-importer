#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.test import TestCase
from data_importer.tasks import DataImpoterTask
from django.contrib.auth.models import User
from data_importer.models_test import Person
from data_importer.importers import CSVImporter
LOCAL_DIR = os.path.dirname(__file__)


class TestMeta(CSVImporter):
    class Meta:
        model = Person
        delimiter = ';'
        ignore_first_line = True


class DataImporterTaskTest(TestCase):

    def setUp(self):
        owner, _ = User.objects.get_or_create(username='test', email='test@test.com')
        self.importer = TestMeta(source=os.path.join(LOCAL_DIR, 'data/person_test.csv'))

        self.task = DataImpoterTask()
        self.task.run(importer=self.importer, owner=owner)

    def test_task_run(self):
        created_person = Person.objects.filter(first_name='Eldo',
                                               last_name='Rock',
                                               age='28').exists()
        self.assertTrue(created_person)

    def test_task_create_all(self):
        self.assertEqual(Person.objects.all().count(), 3)
