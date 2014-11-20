#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.CharField(max_length=10)

    def save(self, force_update=True, *args, **kwargs):
        if force_update:
            return self.full_clean() is None
        super(Person, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.first_name


class PersonFile(models.Model):
    filefield = models.FileField(upload_to='test')

    def __unicode__(self):
        return self.filefield


class Mercado(models.Model):
    item = models.CharField(max_length=50)
    qtde = models.IntegerField(default=0)

    def __unicode__(self):
        return self.item


class Invoice(models.Model):
    name = models.CharField(max_length=50)
    sales_date = models.DateField()
    price = models.FloatField()

    def __unicode__(self):
        return self.name
