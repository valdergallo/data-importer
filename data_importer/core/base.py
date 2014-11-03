#!/usr/bin/env python
import default_settings
DATA_IMPORTER_EXCEL_DECODER = default_settings.DATA_IMPORTER_EXCEL_DECODER
DATA_IMPORTER_DECODER = default_settings.DATA_IMPORTER_DECODER


def objclass2dict(objclass):
    """
    Meta is a objclass on python 2.7 and no have __dict__ attribute.

    This method convert one objclass to one lazy dict without AttributeError
    """
    class Dict(dict):
        def __init__(self, data={}):
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
