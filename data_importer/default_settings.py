#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings

DATA_IMPORTER_TASK = False  # If you need use task data_importer will need install celery
DATA_IMPORTER_QUEUE = "DataImporter"  # Celery Default Queue
DATA_IMPORTER_TASK_LOCK_EXPIRE = 60 * 20  # Lock expires in 20 minutes

DATA_IMPORTER_EXCEL_DECODER = hasattr(settings, 'DATA_IMPORTER_EXCEL_DECODER') and settings.DATA_IMPORTER_EXCEL_DECODER or "cp1252"
DATA_IMPORTER_DECODER = hasattr(settings, 'DATA_IMPORTER_DECODER') and settings.DATA_IMPORTER_DECODER or "utf-8"
