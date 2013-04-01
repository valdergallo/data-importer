#/usr/bin/python
# encoding: utf-8
from data_importer.base import BaseImporter
import xml.etree.cElementTree as et


class XMLImporter(BaseImporter):
    root = 'root'

    def xml_to_dict(self):
        tree = et.fromstring(self.source)
        elements = tree.findall(self.root)
        for el in elements:
            items = el.getchildren()
            content = [i.text for i in items]
            yield content

    def set_reader(self):
        self._reader = self.xml_to_dict()
