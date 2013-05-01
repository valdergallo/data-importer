#!/usr/bin/env python
from setuptools import setup

install_requires = [
    'django>=1.2',
    'openpyxl==1.6.1',
    'xlrd==0.9.0',
    'chardet==2.1.1',
]

setup(name='django-data-importer',
      url='https://github.com/valdergallo/django-data-importer',
      author="valdergallo",
      author_email='valdergallo@gmail.com',
      keywords='Data Importer XLS XLSX CSV XML',
      description='Simple library to easy importer data to django',
      license='MIT',
      classifiers=[
          'Framework :: Django',
          'Operating System :: OS Independent',
          'Topic :: Software Development'
      ],
      version='1.0.0',
      install_requires=install_requires,
      packages=['data_importer', 'data_importer.importers'],
)
