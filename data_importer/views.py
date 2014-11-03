#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .forms import FileUploadForm
from .models import FileHistory
from django.contrib import messages

try:
    from django.views.generic.edit import FormView
except ImportError:
    """
    Add suport to django 1.2
    """
    try:
        from django.views.generic.create_update import create_object as FormView
    except ImportError:
        raise ImportError('Django must be version 1.2 or greater')


class DataImporterForm(FormView):
    """
    Usage example
    ==============

    class DataImporterCreateView(DataImporterForm):
        extra_context = {'title': 'Create Form Data Importer',
                         'template_file': 'myfile.csv'
                        }
        importer_model = MyImporterModel
    """
    model = FileHistory
    template_name = 'data_importer.html'
    form_class = FileUploadForm
    importer = None
    is_task = True
    success_url = '.'
    extra_context = {'title': 'Form Data Importer', 'template_file': 'myfile.csv'}

    def form_valid(self, form, owner=None):
        messages.info(
            self.request,
            "Uploaded file sucess"
        )

        if self.request.user.id:
            owner = self.request.user

        FileHistory.objects.get_or_create(file_uplaod=form.cleaned_data['file_uplaod'],
                                          owner=owner,
                                          content_object=self.importer_model)

        return super(DataImporterForm, self).form_valid(form)
