from collections import namedtuple
from functools import partial, singledispatch   
from typing import NamedTuple, Generic, TypeVar, Any


class vtype(namedtuple('vtype', ['type'])):
    __slots__ = ()

__string=namedtuple('__string', vtype._fields + ('options',))

generic_string      = __string(type=str, options=None)
report_index_type   = __string(type=str, options=['DatetimeIndex', 'datetime', 'date_time'])

class ValidationFailed(Exception):
    pass


def _string_validator(_value, options=None):
    try:
        if _value is None: return _value
        _value = str(_value) # returns the empty string if _value is not provided of string version ('None' if _value is None)
        if _value != '': 
            if type(options) is list: 
                if _value not in options:
                    return ValidationFailed(f'string validator : <{_value}> not match options {options}')
            return _value
    except Exception as e :
        return ValidationFailed(f'string validator unexpected exception : <{e}>')
    else:
        return ValidationFailed(f'string validator error : cannot convert value <{_value}> to string')
    

@singledispatch
def attach_validator(candidate):
    msg = f'<{candidate.__class__.__name__}> MISSING VALIDATOR '
    return False, None, msg


@attach_validator.register(__string)
def _(candidate):
    msg = ''
    try:
        _v = partial(_string_validator, options=candidate.options)
        return True, _v, msg
    except Exception as e:   
        msg += f'<WRONG VALIDATOR> {e} '
        return False, None, msg



vtypes = TypeVar('vtypes', bound=vtype)
class Variable(NamedTuple, Generic[vtypes]):
    vtype : vtypes
    value: Any
    validate : callable = None


class ItemSpec(Variable):
    readonly : bool = False

    def __new__(cls, vtype:vtypes=None, value:Any=None, readonly:bool=False):

        result, _v, msg = attach_validator(vtype)
        if not result:
            raise ValidationFailed(msg)
        
        value = _v(value) 
        if type(value) is ValidationFailed:
            raise ValidationFailed(f'validation failed: {value}')
        
        instance = super().__new__(cls, vtype, value, _v)
        instance.readonly = readonly

        return instance