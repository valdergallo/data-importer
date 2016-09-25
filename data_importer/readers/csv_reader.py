# encoding: utf-8
from __future__ import unicode_literals
import csv

class CSVReader(object):

    def __init__(self, instance, delimiter=';'):
        self.instance = instance
        self.delimiter = delimiter

    def read(self):
        return csv.reader(self.instance.source, delimiter=self.delimiter)
