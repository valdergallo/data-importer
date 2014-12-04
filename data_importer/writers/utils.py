# -*- encoding: utf-8 -*-
from openpyxl import Workbook
from cStringIO import StringIO
from django.core.files import File
import zipfile
try:
    from django.utils import timezone
except ImportError:
    from datatime import datetime as timezone


class QuerysetToWorkbook(object):

    def __init__(self, queryset, columns, filename='report'):
        self.workbook = Workbook(guess_types=True)
        self.sheet = self.workbook.active
        self.queryset = queryset
        self.columns = columns
        self.filename = filename

    def queryset_to_workbook(self):
        if isinstance(self.columns, list) or isinstance(self.columns, tuple):
            self.sheet.append(self.columns)
        for line in self.queryset:
            if hasattr(line, '__dict__'):
                self.sheet.append(line.__dict__.values())
            elif isinstance(line, list) or isinstance(line, tuple):
                self.sheet.append(line)
        return self.workbook

    def get_file(self):
        return self.filename

    def get_content(self):
        in_memory = StringIO()
        wb = self.queryset_to_workbook()
        wb.save(in_memory)
        return in_memory

    def get_compressed_file(self):
        in_memory_zip = StringIO()
        zf = zipfile.ZipFile(in_memory_zip, "w", zipfile.ZIP_DEFLATED)
        zf.writestr(self.get_filename(), self.get_content().getvalue())
        zf.close()
        in_memory_zip.flush()
        return in_memory_zip

    def get_filename(self, username=None, extension='xlsx'):
        if username:
            return self.get_file() + '_' + username + '_' + timezone.now().strftime('%Y%m%d') + '.' + extension
        return self.get_file() + '_' + timezone.now().strftime('%Y%m%d') + '.' + extension

    def compress_django_file(self, compress=True, filename=None):
        return File(self.get_compressed_file())

    def save(self, compress=True, filename=None):
        if compress:
            if not filename:
                filename = self.get_filename(extension='zip')
            with open(filename, 'wb') as fl:
                fl.write(self.get_compressed_file().getvalue())
                return fl
        else:
            if not filename:
                filename = self.get_filename()
            with open(filename, 'wb') as fl:
                fl.write(self.get_file().getvalue())
                return fl

    def response(self, compress=True, filename=None):
        from django.http import HttpResponse

        if compress:
            if not filename:
                filename = self.get_filename(extension='zip')
            response = HttpResponse(mimetype="application/zip")
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            response.write(self.get_compressed_file().getvalue())
        else:
            if not filename:
                filename = self.get_filename()
            response = HttpResponse(mimetype="application/csv")
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            response.write(self.get_file().getvalue())
        return response
