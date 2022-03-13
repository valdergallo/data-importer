# encoding: utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

from example.views import DataImporterCreateView

urlpatterns = (
    patterns(
        "",
        url(r"^$", DataImporterCreateView.as_view(), name="data_importer"),
        # Uncomment the admin/doc line below to enable admin documentation:
        url(r"^admin/doc/", include("django.contrib.admindocs.urls")),
        # Uncomment the next line to enable the admin:
        url(r"^admin/", include(admin.site.urls)),
    )
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
