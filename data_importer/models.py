#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
import os
import tempfile
import zipfile
from datetime import date
import uuid
import django
from distutils.version import StrictVersion

try:
    from django.core.servers.basehttp import FileWrapper
except ImportError:
    from wsgiref.util import FileWrapper

from django.http import HttpResponse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

# port settings.AUTH_USER_MODEL
# from django.contrib.auth import get_user_model
User = settings.AUTH_USER_MODEL

DJANGO_VERSION = StrictVersion(django.get_version())

if DJANGO_VERSION > StrictVersion('1.7'):
    from django.contrib.contenttypes.fields import GenericForeignKey  # for Django > 1.7
else:
    from django.contrib.contenttypes.generic import GenericForeignKey  # for Django < 1.9


DATA_IMPORTER_TASK = hasattr(settings, 'DATA_IMPORTER_TASK') and settings.DATA_IMPORTER_TASK or 0

CELERY_STATUS = ((1, 'Imported'),
                 (2, 'Waiting'),
                 (3, 'Cancelled'),
                 (-1, 'Error'),
                 )


def get_random_filename(instance, filename):
    _, ext = os.path.splitext(filename)
    filename = "{0!s}{1!s}".format(str(uuid.uuid4()), ext)
    user_dir = "anonymous"
    if instance.owner:
        user_dir = instance.owner.get_username()
    return os.path.join('upload_history',
                        user_dir,
                        date.today().strftime("%Y/%m/%d"),
                        filename)


class FileHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, db_index=True)
    file_upload = models.FileField(upload_to=get_random_filename)
    owner = models.ForeignKey(User, null=True)
    is_task = models.BooleanField(default=DATA_IMPORTER_TASK)
    status = models.IntegerField(choices=CELERY_STATUS, default=1)

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name_plural = 'File Histories'

    def file_link(self):
        _url = self.file_upload.url
        return "<a href='{0!s}' tartget='_blank'>Download</a>".format(_url)

    file_link.allow_tags = True

    def download_file(self, request):
        """
        Send a file through Django without loading the whole file into
        memory at once. The FileWrapper will turn the file object into an
        iterator for chunks of 8KB.
        """
        filename = self.file_upload.path
        wrapper = FileWrapper(open(filename, "rb"))
        response = HttpResponse(wrapper, content_type='application/force-download')
        response['Content-Length'] = os.path.getsize(filename)
        return response

    def download_zipfile(self, request):
        """
        Create a ZIP file on disk and transmit it in chunks of 8KB,
        without loading the whole file into memory. A similar approach can
        be used for large dynamic PDF files.
        """
        temp = tempfile.TemporaryFile()
        archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
        for index in range(10):
            filename = self.filename.path
            archive.write(filename, 'file{0:d}.txt'.format(index))
        archive.close()
        wrapper = FileWrapper(temp)
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename={0!s}.zip'.format(self.filename)
        response['Content-Length'] = temp.tell()
        temp.seek(0)
        return response

    @property
    def compose_file_name(self):
        basename = os.path.basename(self.file_upload.file.name)
        return "{0!s} ({1!s})".format(basename, self.owner)
