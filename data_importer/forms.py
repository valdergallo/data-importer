#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from data_importer.models import FileHistory


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileHistory
        fields = ('content',)
