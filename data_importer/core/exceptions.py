#!/usr/bin/env python
# -*- coding: utf-8 -*-

class StopImporter(Exception):
    """
    Stop interator and raise error message
    """


class UnsuportedFile(Exception):
    """
    Unsuported file type
    """


class InvalidModel(Exception):
    """
    Invalid model in descriptor
    """


class InvalidDescriptor(Exception):
    """
    Invalid Descriptor File
    Descriptor must be one valid JSON
    """
