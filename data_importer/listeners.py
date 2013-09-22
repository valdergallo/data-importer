#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models.signals import post_delete
from data_importer.models import FileHistory
import os
from django.conf import settings


def delete_filefield(sender, instance, **kwargs):
    """
    Automatically deleted files when records removed.
    """
    has_delete_config = hasattr(settings, 'DATA_IMPORTER_HISTORY')

    if has_delete_config and settings.DATA_IMPORTER_HISTORY == False:
        if os.path.exists(instance.filename.path):
            os.unlink(instance.filename.path)


post_delete.connect(delete_filefield, sender=FileHistory)
