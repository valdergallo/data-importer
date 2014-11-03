#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et


class XMLReader(object):

    def __init__(self, instance):
        self.instance = instance

    def read(self):
        "Convert XML to Dict"
        tree = et.fromstring(self.instance.source)
        elements = tree.findall(self.instance.root)
        for elem in elements:
            items = list(elem)
            content = [i.text for i in items]
            yield content
