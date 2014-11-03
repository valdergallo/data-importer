#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from django import forms
from .models import FileHistory
from .tasks import DataImpoterTask

try:
    import celery
    HAS_CELERY = True
except ImportError:
    HAS_CELERY = False


class FileUploadForm(forms.ModelForm):
    is_task = True
    importer = None

    class Meta:
        model = FileHistory
        fields = ('filename',)

    def get_mimetype(self, file_history_instance=None):
        filename, extension = os.path.splitext(file_history_instance.file_upload)
        self.mimetype = extension.replace('.', '')
        return self.mimetype

    def _post_clean(self):
        super(FileUploadForm, self)._post_clean()
        if not HAS_CELERY and self.is_task:
            foms.ValidationError("You need install Celery to use Data importer as task")
        elif HAS_CELERY and self.is_task:
            DataImpoterTask.run(self.instance, self.importer)
