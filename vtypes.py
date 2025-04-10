from collections import namedtuple


class VGeneric(namedtuple('VGeneric', ['type'])):
    __slots__ = ()

#vstring=namedtuple('vstring', vgeneric._fields + ('options',))


class VString(VGeneric):
    def __new__(cls, type, options):
        instance = super(VString, cls).__new__(cls, type)
        instance.options = options
        return instance
