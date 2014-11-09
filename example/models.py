#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.CharField(max_length=10)

    def __unicode__(self):
        return self.first_name
