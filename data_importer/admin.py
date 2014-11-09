#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from data_importer.models import FileHistory


class FileAdmin(admin.ModelAdmin):
    list_display = ['compose_file_name', 'updated_at', 'owner',
                    'active', 'is_task', 'status', 'file_link']
    list_filter = ['is_task', 'active', 'status']
    search_fields = ['file_upload']

admin.site.register(FileHistory, FileAdmin)
