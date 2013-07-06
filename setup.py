#!/usr/bin/env python
import os
from setuptools import setup

install_requires = [
    'django>=1.2',
    'openpyxl==1.6.1',
    'xlrd==0.9.0',
]

setup(name='data-importer',
      url='https://github.com/valdergallo/data-importer',
      author="valdergallo",
      author_email='valdergallo@gmail.com',
      keywords='Data Importer XLS XLSX CSV XML',
      description='Simple library to easily import data with Django',
      license='BSD',
      long_description=('''**Django Data Importer** is a tool which allow you to transform easily a CSV, XML, XLS and XLSX file
      into a python object or a django model instance. It is based on the django-style declarative model.'''),
      classifiers=[
          'Framework :: Django',
          'Operating System :: OS Independent',
          'Topic :: Utilities'
      ],
      version='1.0.0b',
      install_requires=install_requires,
      packages=['data_importer', 'data_importer.importers'],
)
