#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import FileHistory


class FileAdmin(admin.ModelAdmin):
    list_display = ['filename', 'created_at', 'updated_at', 'owner',
                    'active', 'is_task', 'status']
    list_filter = ['is_task', 'active', 'status']
    search_fields = ['filename']

admin.site.register(FileHistory, FileAdmin)
