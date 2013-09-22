#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from data_importer.views import DataImporterCreateView, DataImporterUpdateView, DataImporterDeleteView, DataImporterDetailView

urlpatterns = patterns('',
    url(r'^create/', DataImporterCreateView.as_view(), name='create_importer'),
    url(r'^update/(?P<pk>\d+)/$', DataImporterUpdateView.as_view(), name='update_importer'),
    url(r'^delete/(?P<pk>\d+)/$', DataImporterDeleteView.as_view(), name='delete_importer'),
    url(r'^detail/(?P<pk>\d+)/$', DataImporterDetailView.as_view(), name='detail_importer'),
)
