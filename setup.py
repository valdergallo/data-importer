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
        self.test_args = ['data_importer', 'tests', '--cov=data_importer', '-vrsx', '-x']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


install_requires = [
    'django>=1.4',
    'openpyxl==2.4.0',
    'xlrd==1.0.0',
    'six==1.10.0',
]


tests_requires = [
    'pytest==3.0.2',
    'pytest-django==2.9.1',
    'pytest-cov==2.3.1',
    'openpyxl>=2.1.4',
    'xlrd>=1.0.0'
    'django>=1.4',
    'six==1.10.0',
    'mock==2.0.0',
]


setup(
    name='data-importer',
    url='https://github.com/valdergallo/data-importer',
    download_url='https://github.com/valdergallo/data-importer/tarball/{0!s}/'.format(data_importer.__version__),
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
    tests_requires=tests_requires,
    cmdclass={'test': PyTest},
    zip_safe=False,
    platforms='any',
    package_dir={'': '.'},
    packages=find_packages('.', exclude=['tests', '*.tests', 'docs', 'example', 'media']),
    package_data={
        '': ['templates/data_importer.html', 'templates/my_upload.html']
    }
)
