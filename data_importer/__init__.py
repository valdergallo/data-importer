__version__ = '1.0.0'
"""
    Django Data Importer
"""
from .importers.base import BaseImporter
from .importers.xml_importer import XMLImporter
from .importers.xls_importer import XLSImporter
from .importers.xlsx_importer import XLSXImporter
