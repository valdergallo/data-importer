"""
Django migrations for data_importer app

This package does not contain South migrations.  South migrations can be found
in the ``south_migrations`` package.
"""

SOUTH_ERROR_MESSAGE = """\n
For South support, customize the SOUTH_MIGRATION_MODULES setting like so:

    SOUTH_MIGRATION_MODULES = {
        'data_importer': 'data_importer.south_migrations',
    }
"""

# Ensure the user is not using Django 1.6 or below with South
try:
    from django.db import migrations
except ImportError:
    from django.core.exceptions import ImproperlyConfigured

    raise ImproperlyConfigured(SOUTH_ERROR_MESSAGE)
