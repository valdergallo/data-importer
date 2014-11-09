#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from django import forms
from data_importer.models import FileHistory
from data_importer.tasks import DataImpoterTask

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
        fields = ('file_upload',)
