#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .forms import FileUploadForm
from .models import FileHistory
from django.contrib import messages
from data_importer.tasks import DataImpoterTask

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
        importer = MyImporterModel
    """
    model = FileHistory
    template_name = 'data_importer/data_importer.html'
    form_class = FileUploadForm
    task = DataImpoterTask()
    importer = None
    is_task = True
    success_url = '.'
    extra_context = {'title': 'Form Data Importer', 'template_file': 'myfile.csv'}

    def form_valid(self, form, owner=None):
        if self.request.user.id:
            owner = self.request.user

        FileHistory.objects.get_or_create(file_uplaod=form.cleaned_data['file_uplaod'],
                                          owner=owner,
                                          content_object=self.importer.Meta.model)

        if not self.is_task:
            self.task.run(importer=self.importer, owner=owner)
            if self.task.importer.errors:
                messages.error(self.request, self.task.importer.errors)
            else:
                messages.success(self.request, "Uploaded file sucess")
        else:
            self.task.delay(importer=self.importer, owner=owner)
            if owner:
                messages.info(
                    self.request,
                    "When importer was finished one email will send to: %s" % owner.email
                )
            else:
                messages.info(
                    self.request,
                    "Importer task in queue"
                )

        return super(DataImporterForm, self).form_valid(form)
