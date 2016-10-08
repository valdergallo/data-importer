# encoding: utf-8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import data_importer.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, db_index=True)),
                ('file_upload', models.FileField(upload_to=data_importer.models.get_random_filename)),
                ('is_task', models.BooleanField(default=0)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Imported'), (2, b'Waiting'), (3, b'Cancelled'), (-1, b'Error')])),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'File Histories',
            },
            bases=(models.Model,),
        ),
    ]
