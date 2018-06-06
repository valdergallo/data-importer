# encoding: utf-8
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import data_importer


def readme():
    try:
        os.system('pandoc --from=markdown --to=rst README.md -o README.rst')
        with open('README.rst') as f:
            return f.read()
    except Exception:
        return '''**Django Data Importer** is a tool which allow you to transform easily a CSV, XML, XLS and XLSX file into a python object or a django model instance. It is based on the django-style declarative model.'''


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['data_importer', 'tests', '--cov=data_importer', '-vrsx']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='data-importer-sqlalchemy',
    url='https://github.com/valdergallo/data-importer-sqlalchemy',
    download_url='https://github.com/valdergallo/data-importer-sqlalchemy/tarball/{0!s}/'.format(data_importer.__version__),
    author="valdergallo",
    author_email='valdergallo@gmail.com',
    keywords='Data Importer XLS XLSX CSV XML',
    description='Simple library to easily import data with Django',
    license='BSD',
    long_description=readme(),
    classifiers=[
      'Framework :: Django',
      'Framework :: SqlAlchemy',
      'Operating System :: OS Independent',
      'Topic :: Utilities'
    ],
    version=data_importer.__version__,
    install_requires=[
        'SQLAlchemy>=0.9'
        'openpyxl==2.4.0',
        'xlrd==1.1.0',
    ],
    tests_require=[
        'pytest>=3.0.0',
        'xlrd==1.1.0',
        'pytest-cov==2.3.1',
        'openpyxl==2.4.0',
        'six==1.10.0',
        'mock==2.0.0',
    ],
    cmdclass={'test': PyTest},
    zip_safe=False,
    platforms='any',
    package_dir={'': '.'},
    packages=find_packages('.', exclude=['tests', '*.tests', 'docs', 'example', 'media']),
)
