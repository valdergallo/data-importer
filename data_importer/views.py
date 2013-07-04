#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .forms import FileUploadForm
try:
    from django.views.generic.edit import FormView
except:
    pass


class DataImporterGenericView(FormView):
    template_name = 'data_importer.html'
    form_class = FileUploadForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(DataImporterGenericView, self).form_valid(form)
