#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from data_importer.models import FileHistory
try:
    import celery
    HAS_CELERY = True
except ImportError:
    HAS_CELERY = False


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileHistory
        fields = ('content',)

    def _post_clean(self):
        super(FileUploadForm, self)._post_clean()
        if not HAS_CELERY and self.instance.is_task:
            foms.ValidationError("You need install Celery to use Data importer as task")
        elif HAS_CELERY and self.install.is_task:
            # TODO: check File
            # Execute data importer as task
