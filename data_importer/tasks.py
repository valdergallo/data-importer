#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

try:
    from celery import Task
except ImportError:
    Task = object

from django.core.cache import cache
from data_importer import default_settings
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe

try:
    LOCK_EXPIRE = settings.DATA_IMPORTER_TASK_LOCK_EXPIRE
except AttributeError:
    LOCK_EXPIRE = default_settings.DATA_IMPORTER_TASK_LOCK_EXPIRE

try:
    DATA_IMPORTER_QUEUE = settings.DATA_IMPORTER_QUEUE
except AttributeError:
    DATA_IMPORTER_QUEUE = default_settings.DATA_IMPORTER_QUEUE

acquire_lock = lambda lock_id: cache.add(lock_id, "true", LOCK_EXPIRE)
release_lock = lambda lock_id: cache.delete(lock_id)


class DataImpoterTask(Task):
    """
    This tasks is executed by Celery.
    """
    name = 'data_importer_task'
    queue = DATA_IMPORTER_QUEUE
    time_limit = 60 * 15
    mimetype = None
    parse = None

    def run(self, instance=None, importer=None, **kwargs):
        """
        TODO:
            - need create customer messages for tasks
        """
        if not importer or not instance:
            return

        lock_id = "%s-lock" % (self.name)

        if acquire_lock(lock_id):
            parser = importer(instance.file_upload)

            if instance.owner and instance.owner.email:
                email = EmailMessage(subject='[Data Importer] %s was processed' % (os.path.basename(instance.filename.name),),
                     body=mark_safe(parse.errors),
                     to=[instance.owner.email],
                     headers={'Content-Type': 'text/plain'})
            email.send()

            release_lock(lock_id)
        else:
            return 0
