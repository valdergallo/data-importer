#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .forms import FileUploadForm
from .models import FileHistory
from django.contrib import messages

try:
    from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
    from django.views.generic.detail import DetailView
except ImportError:
    """
    Add suport to django 1.2
    """
    try:
        from django.views.generic.create_update import create_object as FormView
        from django.views.generic.create_update import create_object as CreateView
        from django.views.generic.create_update import update_object as UpdateView
        from django.views.generic.create_update import delete_object as DeleteView
        from django.views.generic.date_based import object_detail as DetailView
    except ImportError:
        raise ImportError('Django must be version 1.2 or greater')


class DataImporterDetailView(DetailView):
    model = FileHistory
    template_name = 'data_importer_detail.html'


class DataImporterFormBase(FormView):
    model = FileHistory
    template_name = 'data_importer.html'
    form_class = FileUploadForm
    success_url = '.'
    extra_context = {'title': 'Form Data Importer'}

    # def get(self, *args, **kwargs):
    #     # You can access url variables from kwargs
    #     # url: /email_preferences/geeknam > kwargs['username'] = 'geeknam'
    #     # Assign to self.subscriber to be used later
    #     self.subscriber = get_subscriber(kwargs['username'])

    # def post(self, request, *args, **kwargs):
    #     # Process view when the form gets Posted
    #     pass

    def form_valid(self, form):
        messages.info(
            self.request,
            "Uploaded file sucess"
        )
        FileHistory.objects.get_or_create(filename=form.cleaned_data['filename'])
        return super(DataImporterFormBase, self).form_valid(form)


class DataImporterCreateView(DataImporterFormBase, CreateView):
    extra_context = {'title': 'Create Form Data Importer'}


class DataImporterUpdateView(DataImporterFormBase, UpdateView):
    extra_context = {'title': 'Update Form Data Importer'}


class DataImporterDeleteView(DataImporterFormBase, DeleteView):
    extra_context = {'title': 'Delete Form Data Importer'}
    template_name = 'data_importer_delete.html'
