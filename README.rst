Django Data Importer
====================

.. image:: https://travis-ci.org/valdergallo/django-data-importer.png?branch=master
    :target: https://travis-ci.org/valdergallo/django-data-importer

**Django Data Importer** is a tool which allow you to transform easily a CSV, XML, XLS and XLSX file into a python object or a django model instance. It is based on the django-style declarative model.

.. toctree::
   :maxdepth: 2

Documentation and usage
-----------------------

Read docs online in Read the Docs:

https://django-data-importer.readthedocs.org/


You can generate everything at the above site in your local folder by::

    $ cd doc
    $ make html
    $ open _build/html/index.html # Or your preferred web browser



Installation
------------

Use either ``easy_install``::

    easy_install data-importer

or ``pip``::

    pip install data-importer


Settings
--------

Customize data_importer decoders

**DATA_IMPORTER_EXCEL_DECODER**
 Default value is cp1252

**DATA_IMPORTER_DECODER**
 Default value is UTF-8


Basic example
-------------

Consider the following:

>>> from data_importer.base import BaseImporter
>>> class MyCSVImporterModel(BaseImporter):
...     fields = ['name', 'age', 'length']
...     class Meta:
...         delimiter = ";"

You declare a ``MyCSVImporterModel`` which will match to a CSV file like this:

    Anthony;27;1.75

To import the file or any iterable object, just do:

>>> my_csv_list = MyCSVImporterModel(source="my_csv_file_name.csv")
>>> row, first_line = my_csv_list.cleaned_data[0]
>>> first_line['age']
27

Without an explicit declaration, data and columns are matched in the same
order::

    Anthony --> Column 0 --> Field 0 --> name
    27      --> Column 1 --> Field 1 --> age
    1.75    --> Column 2 --> Field 2 --> length

Django Model
------------

If you now want to interact with a django model, you just have to add a **Meta.model** option to the class meta.

>>> from django.db import models
>>> class MyModel(models.Model):
...     name = models.CharField(max_length=150)
...     age = models.CharField(max_length=150)
...     length = models.CharField(max_length=150)

>>> from data_importer.base import BaseImporter
>>> from data_importer.model import MyModel
>>> class MyCSVImporterModel(BaseImporter):
...     class Meta:
...         delimiter = ";"
...         model = MyModel

That will automatically match to the following django model.

*The django model should be imported in the model*

.. py:class:: Meta

    **delimiter**
        define the delimiter of the csv file.
        If you do not set one, the sniffer will try yo find one itself.

    **ignore_first_line**
        Skip the first line if True.

    **model**
        If defined, the importer will create an instance of this model.

    **raise_errors**
        If set to True, an error in a imported line will stop the loading.

    **exclude**
        Exclude fields from list fields to import

    **transaction** `(beta) not tested`
        Use transaction to save objects


Django XML
------------

If you now want to interact with a django model, you just have to add a **Meta.model** option to the class meta.

XML file example:

.. code-block:: guess

    <encspot>
      <file>
       <Name>Rocky Balboa</Name>
       <Age>40</Age>
       <Height>1.77</Height>
      </file>
      <file>
       <Name>Chuck Norris</Name>
       <Age>73</Age>
       <Height>1.78</Height>
      </file>
    </encspot>

>>> from django.db import models
>>> class MyModel(models.Model):
...     name = models.CharField(max_length=150)
...     age = models.CharField(max_length=150)
...     height = models.CharField(max_length=150)

>>> from data_importer import XMLImporter
>>> from data_importer.model import MyModel
>>> class MyCSVImporterModel(XMLImporter):
...     root = 'file'
...     class Meta:
...         model = MyModel

That will automatically match to the following django model.

*The django model should be imported in the model*



.. py:class:: Meta

    **model**
        If defined, the importer will create an instance of this model.

    **raise_errors**
        If set to True, an error in a imported line will stop the loading.

    **exclude**
        Exclude fields from list fields to import

    **transaction** `(beta) not tested`
        Use transaction to save objects


Django XLS/XLSX
----------------

My XLS/XLSX file can be imported too

+---------+---------+---------+---------+
| Header1 | Header2 | Header3 | Header4 |
+=========+=========+=========+=========+
| Teste 1 | Teste 2 | Teste 3 | Teste 4 |
+---------+---------+---------+---------+
| Teste 1 | Teste 2 | Teste 3 | Teste 4 |
+---------+---------+---------+---------+


This is my model

>>> from django.db import models
>>> class MyModel(models.Model):
...     header1 = models.CharField(max_length=150)
...     header2 = models.CharField(max_length=150)
...     header3 = models.CharField(max_length=150)
...     header4 = models.CharField(max_length=150)

This is my class

>>> from data_importer import XLSImporter
>>> from data_importer.model import MyModel
>>> class MyXLSImporterModel(XLSImporter):
...     class Meta:
...         model = MyModel

If you are using XLSX you will need use XLSXImporter to made same importer

>>> from data_importer import XLSXImporter
>>> from data_importer.model import MyModel
>>> class MyXLSXImporterModel(XLSXImporter):
...     class Meta:
...         model = MyModel

.. py:class:: Meta

    **ignore_first_line**
        Skip the first line if True.

    **model**
        If defined, the importer will create an instance of this model.

    **raise_errors**
        If set to True, an error in a imported line will stop the loading.

    **exclude**
        Exclude fields from list fields to import

    **transaction** `(beta) not tested`
        Use transaction to save objects

TEST
----

+----------------------+----------------+-----+
|Acentuation with XLS  | Excel MAC 2011 | OK  |
+----------------------+----------------+-----+
|Acentuation with XLSX | Excel MAC 2011 | OK  |
+----------------------+----------------+-----+
|Acentuation with CSV  | Excel Win 2007 | OK  |
+----------------------+----------------+-----+


TODO
____
    ** MORE DOCS **

