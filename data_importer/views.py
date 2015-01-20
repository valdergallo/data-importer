#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data_importer.forms import FileUploadForm
from data_importer.models import FileHistory
from django.contrib import messages
from data_importer.tasks import DataImpoterTask
from django.contrib.contenttypes.models import ContentType

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
    template_name = 'data_importer.html'
    form_class = FileUploadForm
    task = DataImpoterTask()
    importer = None
    is_task = True
    success_url = '.'
    extra_context = {'title': 'Form Data Importer', 'template_file': 'myfile.csv'}

    def get_context_data(self, **kwargs):
        context = super(DataImporterForm, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

    def form_valid(self, form, owner=None):
        if self.request.user.id:
            owner = self.request.user

        content_type = ContentType.objects.get_for_model(self.importer.Meta.model)
        file_history, _ = FileHistory.objects.get_or_create(file_upload=form.cleaned_data['file_upload'],
                                                            owner=owner,
                                                            content_type=content_type)

        if not self.is_task or not hasattr(self.task, 'delay'):
            self.task.run(importer=self.importer,
                          source=file_history,
                          owner=owner,
                          send_email=False)
            if self.task.parser.errors:
                messages.error(self.request, self.task.parser.errors)
            else:
                messages.success(self.request, "File uploaded successfully")
        else:
            self.task.delay(importer=self.importer, source=file_history, owner=owner)
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
