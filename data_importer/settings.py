#!/usr/bin/env python
# -*- coding: utf-8 -*-

DATA_IMPORTER_TASK = False  # If you need use task data_importer will need install celery
DATA_IMPORTER_QUEUE = "DataImporter"  # Celery Default Queue
LOCK_EXPIRE = 60 * 20  # Lock expires in 20 minutes
