#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

try:
    from celery import Task
except ImportError:
    Task = object

from django.core.cache import cache
from data_importer.core import default_settings
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe

try:
    from django.conf import settings
except ImportError, e:
    settings = None

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

    @staticmethod
    def send_email(subject='[Data Importer] was processed', body="", owner=None):
        email = EmailMessage(subject=subject,
                             body=body,
                             to=[owner.email],
                             headers={'Content-Type': 'text/plain'})
        email.send()

    def run(self, importer=None, source="", owner=None, message="",
            send_email=True, **kwargs):
        if not importer:
            return

        self.parser = importer(source=source)

        lock_id = "%s-lock" % (self.name)

        if acquire_lock(lock_id):
            """
            If parser use raise_errors the error message will raise
            and logged by celery
            """
            # validate content
            self.parser.is_valid()
            # save valid values
            self.parser.save()

            message += "\n"

            if owner and owner.email and self.parser.errors:
                message += mark_safe(self.parser.errors)
            elif owner and owner.email and not self.parser.errors:
                message = "Your file was imported with sucess"

            if hasattr(owner, 'email') and send_email:
                self.send_email(body=message, owner=owner)

            release_lock(lock_id)
        else:
            return 0
