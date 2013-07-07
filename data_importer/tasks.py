#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import os

try:
    from celery import Task
except ImportError:
    Task = object

from django.core.cache import cache
from data_importer import BaseImporter, XMLImporter, XLSImporter, XLSXImporter
from django.conf import settings
from data_importer import settings as data_importer_settings

LOCK_EXPIRE = hasattr(settings, 'DATA_IMPORTER_TASK_LOCK_EXPIRE') and settings.DATA_IMPORTER_TASK_LOCK_EXPIRE or data_importer_settings.DATA_IMPORTER_TASK_LOCK_EXPIRE

DATA_IMPORTER_QUEUE = hasattr(settings, 'DATA_IMPORTER_QUEUE') and settings.DATA_IMPORTER_QUEUE or data_importer_settings.DATA_IMPORTER_QUEUE

acquire_lock = lambda lock_id: cache.add(lock_id, "true", LOCK_EXPIRE)
release_lock = lambda lock_id: cache.delete(lock_id)


class DataImpoterTask(Task):
    """
    This tasks is executed by Celery.
    """
    name = 'flowbot.add_pending_jobs_to_flowbot'
    queue = DATA_IMPORTER_QUEUE
    time_limit = 60 * 15
    mimetype = None

    def get_mimetype(self, file_history_instance=None):
        filename, extension = os.path.splitext(file_history_instance.filename)
        self.mimetype = extension.replace('.', '')
        return self.mimetype

    def parse_xml(self, file_history_instance):
        XMLImporter(file_history_instance)

    def parse_csv(self, file_history_instance):
        BaseImporter(file_history_instance)

    def parse_xls(self, file_history_instance):
        XLSImporter(file_history_instance)

    def parse_xlsx(self, file_history_instance):
        XLSXImporter(file_history_instance)

    def get_parser(self):
        function_name = 'parse_%s' % self.mimetype
        return getattr(self, function_name)

    def run(self, instance, **kwargs):
        logger = self.get_logger(**kwargs)
        lock_id = "%s-lock" % (self.name)
        errors = []

        if acquire_lock(lock_id):
            mime_type = self.get_mimetype(instance)
            parse_instance = self.get_parser(mime_type)
            parse_instance(instance)
            release_lock(lock_id)
            logger.info("TASK FINISH: %s %s" % (lock_id, datetime.now()))
        else:
            logger.info('TASK LOCKED: %s' % (datetime.now()))
            return 0
