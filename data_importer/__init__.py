"""
    Django Data Importer
"""

__version__ = '1.0.0'
__author__ = 'Valder Gallo <valdergallo@gmail.com>'


from .importers.base import BaseImporter
from .importers.xml_importer import XMLImporter
from .importers.xls_importer import XLSImporter
from .importers.xlsx_importer import XLSXImporter
