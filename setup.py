#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
import os
from setuptools import setup, find_packages

import data_importer


def readme():
    try:
        os.system('pandoc --from=markdown --to=rst README.md -o README.rst')
        with open('README.rst') as f:
            return f.read()
    except:
        return '''**Django Data Importer** is a tool which allow you to transform easily a CSV, XML, XLS and XLSX file into a python object or a django model instance. It is based on the django-style declarative model.'''


install_requires = [
    'django>=1.4',
    'openpyxl>=2.1.4',
    'xlrd>=0.9.3',
]


setup(
    name='data-importer',
    url='https://github.com/valdergallo/data-importer',
    download_url='https://github.com/valdergallo/data-importer/tarball/%s/' % data_importer.__version__,
    author="valdergallo",
    author_email='valdergallo@gmail.com',
    keywords='Django Data Importer XLS XLSX CSV XML',
    description='Simple library to easily import data with Django',
    license='BSD',
    long_description=readme(),
    classifiers=[
      'Framework :: Django',
      'Operating System :: OS Independent',
      'Topic :: Utilities'
    ],
    version=data_importer.__version__,
    install_requires=install_requires,
    package_dir={'': '.'},
    packages=find_packages('.', exclude=['tests', '*.tests', 'docs', 'example', 'media']),
    package_data={
        '': ['templates/data_importer.html', 'templates/my_upload.html']
    }
)
