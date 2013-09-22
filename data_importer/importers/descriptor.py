#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
try:
    import json
except ImportError:
    import simplejson as json


class ReadDescriptor(object):

    def __init__(self, file_name=None, model_name=None):
        self.file_name = file_name
        self.model_name = model_name
        self.source = None

        self.read_file()

    def read_file(self):
        if not os.path.exists(self.file_name):
            raise ValueError('Invalid JSON File Source')

        read_file = open(self.file_name, 'r')
        self.source = json.loads(read_file.read())

    def get_model(self):
        valid_model = [i for i in self.source if self.model_name in i.get('model')]
        if not valid_model:
            raise ValueError("Model Name does not exist in descriptor")

        return valid_model[0]

    def get_fields(self):
        model = self.get_model()
        return model.get('fields').keys()
