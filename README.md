Django Data Importer
====================

![image](https://travis-ci.org/valdergallo/data-importer.png?branch=master%0A%20:target:%20https://travis-ci.org/valdergallo/data-importer)

![image](http://img.shields.io/pypi/v/data-importer.svg%0A%20:target:%20https://pypi.python.org/pypi/data-importer)

![image](https://pypip.in/d/data-importer/badge.png%0A%20:target:%20https://www.djangopackages.com/packages/p/data-importer/)

![image](http://img.shields.io/badge/license-BSD-yellow.svg%0A%20:target:%20http://opensource.org/licenses/BSD-3-Clause)

**Django Data Importer** is a tool which allow you to transform easily a
CSV, XML, XLS and XLSX file into a python object or a django model
instance. It is based on the django-style declarative model.

Documentation and usage
-----------------------

Read docs online in Read the Docs:

<https://django-data-importer.readthedocs.org/>

You can generate everything at the above site in your local folder by:

    $ cd doc
    $ make html
    $ open _build/html/index.html # Or your preferred web browser

Installation
------------

Use either `easy_install`:

    easy_install data-importer

or `pip`:

    pip install data-importer

Settings
--------

Customize data\_importer decoders

**DATA\_IMPORTER\_EXCEL\_DECODER**
:   Default value is cp1252

**DATA\_IMPORTER\_DECODER**
:   Default value is UTF-8

Basic example
-------------

Consider the following:

\>\>\> from data\_importer.importers import CSVImporter \>\>\> class
MyCSVImporterModel(CSVImporter): ... fields = ['name', 'age', 'length']
... class Meta: ... delimiter = ";"

You declare a `MyCSVImporterModel` which will match to a CSV file like
this:

> Anthony;27;1.75

To import the file or any iterable object, just do:

\>\>\> my\_csv\_list =
MyCSVImporterModel(source="my\_csv\_file\_name.csv") \>\>\> row,
first\_line = my\_csv\_list.cleaned\_data[0] \>\>\> first\_line['age']
27

Without an explicit declaration, data and columns are matched in the
same order:

    Anthony --> Column 0 --> Field 0 --> name
    27      --> Column 1 --> Field 1 --> age
    1.75    --> Column 2 --> Field 2 --> length

Django Model
------------

If you now want to interact with a django model, you just have to add a
**Meta.model** option to the class meta.

\>\>\> from django.db import models \>\>\> class MyModel(models.Model):
... name = models.CharField(max\_length=150) ... age =
models.CharField(max\_length=150) ... length =
models.CharField(max\_length=150)

\>\>\> from data\_importer.importers import CSVImporter \>\>\> from
data\_importer.model import MyModel \>\>\> class
MyCSVImporterModel(CSVImporter): ... class Meta: ... delimiter = ";" ...
model = MyModel

That will automatically match to the following django model.

*The django model should be imported in the model*

Django XML
----------

If you now want to interact with a django model, you just have to add a
**Meta.model** option to the class meta.

XML file example:

~~~~ {.sourceCode .guess}
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
~~~~

\>\>\> from django.db import models \>\>\> class MyModel(models.Model):
... name = models.CharField(max\_length=150) ... age =
models.CharField(max\_length=150) ... height =
models.CharField(max\_length=150)

\>\>\> from data\_importer.importers import XMLImporter \>\>\> from
data\_importer.model import MyModel \>\>\> class
MyCSVImporterModel(XMLImporter): ... root = 'file' ... class Meta: ...
model = MyModel

That will automatically match to the following django model.

*The django model should be imported in the model*

Django XLS/XLSX
---------------

My XLS/XLSX file can be imported too

  Header1    Header2    Header3    Header4
  ---------- ---------- ---------- ----------
  Teste 1    Teste 2    Teste 3    Teste 4
  Teste 1    Teste 2    Teste 3    Teste 4

This is my model

\>\>\> from django.db import models \>\>\> class MyModel(models.Model):
... header1 = models.CharField(max\_length=150) ... header2 =
models.CharField(max\_length=150) ... header3 =
models.CharField(max\_length=150) ... header4 =
models.CharField(max\_length=150)

This is my class

\>\>\> from data\_importer import XLSImporter \>\>\> from
data\_importer.model import MyModel \>\>\> class
MyXLSImporterModel(XLSImporter): ... class Meta: ... model = MyModel

If you are using XLSX you will need use XLSXImporter to made same
importer

\>\>\> from data\_importer import XLSXImporter \>\>\> from
data\_importer.model import MyModel \>\>\> class
MyXLSXImporterModel(XLSXImporter): ... class Meta: ... model = MyModel

Descriptor
----------

Using file descriptor to define fields for large models.

import\_test.json

~~~~ {.sourceCode .javascript}
{
  'app_name': 'mytest.Contact',
    {
    // field name / name on import file or key index
    'name': 'My Name',
    'year': 'My Year',
    'last': 3
    }
}
~~~~

model.py

~~~~ {.sourceCode .python}
class Contact(models.Model):
  name = models.CharField(max_length=50)
  year = models.CharField(max_length=10)
  laster = models.CharField(max_length=5)
  phone = models.CharField(max_length=5)
  address = models.CharField(max_length=5)
  state = models.CharField(max_length=5)
~~~~

importer.py

~~~~ {.sourceCode .python}
class MyImpoter(BaseImpoter):
  class Meta:
    config_file = 'import_test.json'
    model = Contact
    delimiter = ','
    ignore_first_line = True
~~~~

content\_file.csv

~~~~ {.sourceCode .guest}
name,year,last
Test,12,1
Test2,13,2
Test3,14,3
~~~~

Default DataImporterForm
------------------------

DataImporterForm is one django.views.generic.edit.FormView to save file
in FileUpload and parse content on success.

Example
-------

~~~~ {.sourceCode .guest}
class DataImporterCreateView(DataImporterForm):
    extra_context = {'title': 'Create Form Data Importer',
                     'template_file': 'myfile.csv'
                    }
    importer = MyCSVImporterModel
~~~~

TEST
----

  ------------------------ --------------------- ------
  Acentuation with XLS     Excel MAC 2011        OK
  Acentuation with XLS     Excel WIN 2010        OK
  Acentuation with XLSX    Excel MAC 2011        OK
  Acentuation with XLSX    Excel WIN 2010        OK
  Acentuation with CSV     Excel Win 2010        OK
  ------------------------ --------------------- ------

* * * * *

> Python
> :   python 2.7
>
> Django
> :   1.2+
>

