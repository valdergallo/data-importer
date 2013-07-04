#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
import os
import tempfile
import zipfile
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse


class FileHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, db_index=True)
    content = models.FileField(upload_to="upload_history/%Y/%m/%d/")

    def send_file(self, request):
        """
        Send a file through Django without loading the whole file into
        memory at once. The FileWrapper will turn the file object into an
        iterator for chunks of 8KB.
        """
        filename = self.content
        wrapper = FileWrapper(file(filename))
        response = HttpResponse(wrapper, content_type='text/plain')
        response['Content-Length'] = os.path.getsize(filename)
        return response

    def send_zipfile(self, request):
        """
        Create a ZIP file on disk and transmit it in chunks of 8KB,
        without loading the whole file into memory. A similar approach can
        be used for large dynamic PDF files.
        """
        temp = tempfile.TemporaryFile()
        archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
        for index in range(10):
            filename = self.content
            archive.write(filename, 'file%d.txt' % index)
        archive.close()
        wrapper = FileWrapper(temp)
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=%s.zip' % self.content.basename
        response['Content-Length'] = temp.tell()
        temp.seek(0)
        return response
