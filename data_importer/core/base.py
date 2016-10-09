from __future__ import absolute_import, unicode_literals
from . import default_settings
DATA_IMPORTER_EXCEL_DECODER = default_settings.DATA_IMPORTER_EXCEL_DECODER
DATA_IMPORTER_DECODER = default_settings.DATA_IMPORTER_DECODER


def objclass2dict(objclass):
    """
    Meta is a objclass on python 2.7 and no have __dict__ attribute.

    This method convert one objclass to one lazy dict without AttributeError
    """
    class Dict(dict):
        def __init__(self, data=None):
            if data is None:
                data = {}
            super(Dict, self).__init__(data)
            self.__dict__ = dict(self.items())

        def __getattr__(self, key):
            try:
                return self.__getattribute__(key)
            except AttributeError:
                return False

    obj_list = [i for i in dir(objclass) if not str(i).startswith("__")]
    obj_values = []
    for objitem in obj_list:
        obj_values.append(getattr(objclass, objitem))
    return Dict(zip(obj_list, obj_values))


def convert_alphabet_to_number(letters):
    letters = str(letters).lower()
    if letters.isdigit():
        return int(letters)
    result = ''
    for letter in letters:
        number = (ord(letter) - 96)
        result += str(number)
    # -1 to get zero in list items
    return int(result) - 1


def reduce_list(key_list, values_list):
    new_list = []
    for key in key_list:
        try:
            v = values_list[key]
        except IndexError:
            continue
        new_list.append(v)
    return new_list
