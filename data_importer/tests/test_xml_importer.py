# encoding: utf-8
from __future__ import unicode_literals
import os
from django.test import TestCase
from django.db import models
from data_importer.importers.xml_importer import XMLImporter
LOCAL_DIR = os.path.dirname(__file__)

sxml = os.path.join(LOCAL_DIR, 'data/test_music.xml')


class Musics(models.Model):
    name = models.CharField(max_length=100)
    encoder = models.CharField(max_length=100)
    bitrate = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        return self.full_clean() is None


class TestXMLImporter(TestCase):

    def setUp(self):
        class TestXML(XMLImporter):
            root = 'file'
            fields = ['name', 'encoder', 'bitrate']

        self.importer = TestXML(source=sxml)

    def test_read_content(self):
        self.assertEquals(self.importer.cleaned_data[0], (1, {'bitrate': '131',
                          'name': 'some filename.mp3', 'encoder': 'Gogo (after 3.0)'}))

    def test_values_is_valid(self):
        self.assertTrue(self.importer.is_valid())


class TestXMLCleanImporter(TestCase):

    def setUp(self):
        class TestXML(XMLImporter):
            root = 'file'
            fields = ['name', 'encoder', 'bitrate']

            def clean_name(self, value):
                return str(value).upper()

        self.importer = TestXML(source=sxml)

    def test_read_content(self):
        self.assertEquals(self.importer.cleaned_data[0], (1, {'bitrate': '131',
                          'name': 'SOME FILENAME.MP3', 'encoder': 'Gogo (after 3.0)'}))

    def test_values_is_valid(self):
        self.assertTrue(self.importer.is_valid())


class TestXMLModelImporter(TestCase):

    def setUp(self):
        class TestXML(XMLImporter):
            root = 'file'

            class Meta:
                model = Musics

            def clean_name(self, value):
                return str(value).upper()

        self.importer = TestXML(source=sxml)

    def test_model_fields(self):
        self.assertEquals(self.importer.fields, ['name', 'encoder', 'bitrate'])

    def test_read_content(self):
        content = {'bitrate': '131',
        'encoder': 'Gogo (after 3.0)',
        'name': 'SOME FILENAME.MP3'}
        self.assertEquals(self.importer.cleaned_data[0], (1, content))

    def test_values_is_valid(self):
        self.assertTrue(self.importer.is_valid())

    def test_save_data(self):
        for row, data in self.importer.cleaned_data:
            instace = Musics(**data)
            self.assertTrue(instace.save())
