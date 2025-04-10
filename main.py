import platform
from pathlib import Path, WindowsPath #, PosixPath

pyversion = platform.python_version()


def f1():
    from collections import namedtuple
    from functools import singledispatch, partial
    from typing import Generic, NamedTuple, TypeVar

    __string = namedtuple('__string', ['options'])

    class Generics(NamedTuple, Generic[TypeVar('T')]):
        pass

    
    class TypeDefs(Generics):
        pass

    class _type(Generics):
        template : namedtuple
        def __repr__(self):
            return f"test({self.__class__.__name__})"
        
        def __init__(self, template: namedtuple):
            self.template = template
            

    test = _type(__string(['foo', 'bar']))

    '''__string = namedtuple('__string', ['options'])
    generic_string = __string(typ=str, options=None)'''


def f2():
    from v1 import (
        generic_string,
        report_index_type,
        attach_validator,
        ValidationFailed,
        ItemSpec,

    )

    foo = report_index_type

    print(f"foo: {foo}")

    try:
        result, v, msg = attach_validator(foo)
        if result:
            ri = v('datetime')
        if type(ri) is ValidationFailed:
            raise ri

    except ValidationFailed as e:
        print(f"Exception: {e}")
    else:
        print(f"(OK) ri: {ri}")


    config = {'foo': ItemSpec(report_index_type, 'datetime', readonly=True)}

    print(f'config[foo].vtype: {config["foo"].vtype}')
    print(f'config[foo].value: {config["foo"].value}')
    print(f'config[foo].readonly: {config["foo"].readonly}')


def f3():
    from vtypes import VString, VPath
    from itemspecs import ItemSpec
    from collections import namedtuple

    report_index_type   = VString(type=str, options=['DatetimeIndex', 'datetime', 'date_time'])
    effective_path      = VPath(type=WindowsPath if platform.system() == 'Windows' else Path, cast=True, exist=True)

    config = {'index': ItemSpec(report_index_type, 'datetime', readonly=True),
              'current_path' : ItemSpec(effective_path, __file__)}

    app_index = config["index"]
    print(f'config[index].vtype     : {app_index.vtype}')
    print(f'config[index].value     : {app_index.value}')
    print(f'config[index].readonly  : {app_index.readonly}')

    current_path = config["current_path"]

    print(f"current path = {current_path.value}")
    print(f"of type <{current_path.vtype}>")


def f4():
    from collections import namedtuple

    class vgeneric(namedtuple('vtype', ['type'])):
        __slots__ = ()

    class vstring(vgeneric):
        def __new__(cls, type, options):
            instance = super(vstring, cls).__new__(cls, type)
            instance.options = options
            return instance

    # Esempio di utilizzo
    v = vstring(type='example_type', options='example_options')
    print(v.type)      # Output: example_type
    print(v.options)   # Output: example_options



if __name__ == "__main__":

    print(f"python version: {pyversion}")

    f3()
    
    