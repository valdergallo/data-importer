Views
=====

DataImporterForm
================

    Is a mixin of `django.views.generic.edit.FormView` with default template and form
    to upload files and importent content.

    :Parameters:
    :model:  Model where the file will be save

                 *By default this values is FileHistory*
    :template_name: Template name to be used with FormView

                 *By default is data_importer/data_importer.html*
    :form_class: Form that will be used to upload file
                 
                 *By default this value is FileUploadForm*
    :task: Task that will be used to parse file imported

                 *By default this value is DataImpoterTask*

    :importer: Must be one data_importer.importers class that will be used to validate data.

    :is_task: Use importer in async mode.
    
    :success_url: Redirect to success page after importer
    
    :extra_context: Set extra context values in template


Usage example
==============

.. code-block:: python

    class DataImporterCreateView(DataImporterForm):
        extra_context = {'title': 'Create Form Data Importer',
                         'template_file': 'myfile.csv'}
        importer = MyImporterModel