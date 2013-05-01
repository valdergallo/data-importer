#!/usr/bin/env python
import os
from setuptools import setup

install_requires = [
    'django>=1.2',
    'openpyxl==1.6.1',
    'xlrd==0.9.0',
    'chardet==2.1.1',
]

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='django-data-importer',
      url='https://github.com/valdergallo/django-data-importer',
      author="valdergallo",
      author_email='valdergallo@gmail.com',
      keywords='Data Importer XLS XLSX CSV XML',
      description='Simple library to easy importer data with Django',
      license='BSD',
      long_description=read('README.rst'),
      classifiers=[
          'Framework :: Django',
          'Operating System :: OS Independent',
          'Topic :: Utilities'
          "License :: OSI Approved :: BSD License",
      ],
      version='1.0.0',
      install_requires=install_requires,
      packages=['data_importer', 'data_importer.importers'],
)
