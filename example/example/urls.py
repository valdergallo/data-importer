#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from data_importer.views import DataImporterCreateView, DataImporterUpdateView, DataImporterDeleteView, DataImporterDetailView

urlpatterns = patterns('',
    #: Example
    url(r'^create/', DataImporterCreateView.as_view(), name='create_importer'),
    url(r'^update/(?P<pk>\d+)/$', DataImporterUpdateView.as_view(), name='update_importer'),
    url(r'^delete/(?P<pk>\d+)/$', DataImporterDeleteView.as_view(), name='delete_importer'),
    url(r'^detail/(?P<pk>\d+)/$', DataImporterDetailView.as_view(), name='detail_importer'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
