#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseImporter
import xml.etree.ElementTree as et

class XMLImporter(BaseImporter):
    """
    Import XML files
    """
    root = 'root'

    def xml_to_dict(self):
        "Convert XML to Dict"
        tree = et.fromstring(self.source)
        elements = tree.findall(self.root)
        for elem in elements:
            items = list(elem)
            content = [i.text for i in items]
            yield content

    def set_reader(self):
        self._reader = self.xml_to_dict()
