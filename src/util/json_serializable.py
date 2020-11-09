""" Module that monkey-patches the json module when it's imported so
JSONEncoder.default() automatically checks to see if the object being encoded
is an instance of an Enum type and, if so, returns its name.
"""
from enum import Enum
from json import JSONEncoder

_saved_default = JSONEncoder().default  # Save default method.

def _new_default(self, obj):
    if isinstance(obj, Enum):
        return obj.name  # Could also be obj.value
    else:
        return _saved_default

JSONEncoder.default = _new_default # Set new default method.