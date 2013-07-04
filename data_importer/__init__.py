#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Django Data Importer
"""

__version__ = '1.0.0b'
__author__ = 'Valder Gallo <valdergallo@gmail.com>'


from .importers.base import BaseImporter
from .importers.xml_importer import XMLImporter
from .importers.xls_importer import XLSImporter
from .importers.xlsx_importer import XLSXImporter
