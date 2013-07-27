#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .forms import FileUploadForm
from .models import FileHistory
from django.contrib import messages
try:
    from django.views.generic.edit import FormView, CreateView, UpdateView
except ImportError:
    try:
        from django.views.generic.create_update import create_object as FormView
    except ImportError:
        pass


class DataImporterFormView(FormView):
    template_name = 'data_importer.html'
    form_class = FileUploadForm
    success_url = '.'
    extra_context = {'title': 'Data Importer'}

    # def get(self, *args, **kwargs):
    #     # You can access url variables from kwargs
    #     # url: /email_preferences/geeknam > kwargs['username'] = 'geeknam'
    #     # Assign to self.subscriber to be used later
    #     self.subscriber = get_subscriber(kwargs['username'])

    # def post(self, request, *args, **kwargs):
    #     # Process view when the form gets POSTed
    #     pass

    def form_valid(self, form):
        messages.info(
            self.request,
            "Uploaded file sucess"
        )
        FileHistory.objects.get_or_create(filename=form.cleaned_data['filename'])
        return super(DataImporterFormView, self).form_valid(form)


class DataImporterCreateView(CreateView):
    template_name = 'data_importer.html'
    model = FileHistory
    success_url = '.'
    extra_context = {'title': 'Data Importer'}


class DataImporterUpdateView(UpdateView):
    template_name = 'data_importer.html'
    model = FileHistory
    success_url = '.'
    extra_context = {'title': 'Data Importer'}
