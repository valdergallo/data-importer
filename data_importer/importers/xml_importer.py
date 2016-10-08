# encoding: utf-8
from __future__ import unicode_literals
from data_importer.importers.base import BaseImporter
from data_importer.readers.xml_reader import XMLReader


class XMLImporter(BaseImporter):
    """
    Import XML files
    """
    root = 'root'

    def set_reader(self):
        self._reader = XMLReader(self)
