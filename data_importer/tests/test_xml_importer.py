#/usr/bin/python
# encoding: utf-8
from django.test import TestCase
from ..base import BaseImporter
from cStringIO import StringIO
from django.db import models
from ..xml_reader import XMLImporter

sxml="""
<encspot>
  <file>
   <Name>some filename.mp3</Name>
   <Encoder>Gogo (after 3.0)</Encoder>
   <Bitrate>131</Bitrate>
  </file>
  <file>
   <Name>another filename.mp3</Name>
   <Encoder>iTunes</Encoder>
   <Bitrate>128</Bitrate>
  </file>
</encspot>
"""


class TestXMLImporter(TestCase):

    def setUp(self):
        class TestXML(XMLImporter):
            root = 'file'
            fields = ['name', 'encoder', 'bitrate']

        self.importer = TestXML(source=sxml)

    def test_read_content(self):
        self.assertEquals(self.importer.cleaned_data[0], (0, {'bitrate': '131',
                          'name': 'some filename.mp3', 'encoder': 'Gogo (after 3.0)'}))
