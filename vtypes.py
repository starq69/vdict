from collections import namedtuple
from typing import TypeVar

#managed_types =()

class VGeneric(namedtuple('VGeneric', ['type'])):
    __slots__ = ()

'''VString=namedtuple('VString', VGeneric._fields + ('options',))
managed_types += (VString,)
vtypes = TypeVar('vtypes', *managed_types)
'''

class VString(VGeneric):
    def __new__(cls, type, options):
        i = super().__new__(cls, type)
        i.options = options if options else []
        return i

class VPath(VGeneric):
    def __new__(cls, type, cast=True, exist=True):
        i = super().__new__(cls, type)
        i.cast  = cast
        i.exist = exist
        return i
