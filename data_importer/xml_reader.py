#/usr/bin/python
# encoding: utf-8
from data_importer.base import BaseImporter

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


class XMLImporter(BaseImporter):
    root = 'file'
    fields = [
        'name', 'encoder', 'bitrate'
    ]

    def set_reader(self):
        tree = et.fromstring(self.source)
        self._reader =
