#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from data_importer.core.exceptions import InvalidModel, InvalidDescriptor
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
        "Read json file"
        if not os.path.exists(self.file_name):
            raise InvalidDescriptor('Invalid JSON File Source')

        read_file = open(self.file_name, 'r')
        self.source = json.loads(read_file.read())

    def get_model(self):
        "Read model from JSON descriptor"
        valid_model = [i for i in self.source if self.model_name in i.get('model')]
        if not valid_model:
            raise InvalidModel("Model Name does not exist in descriptor")

        return valid_model[0]

    def get_fields(self):
        "Get content"
        model = self.get_model()
        fields = model.get('fields')
        if isinstance(fields, dict):
            fields = fields.keys()
        return fields
