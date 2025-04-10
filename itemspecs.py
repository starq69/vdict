from collections import namedtuple
from typing import NamedTuple, Generic, TypeVar, Any

from validation import ValidationFailed, attach_validator
from vtypes import VGeneric


vtypes = TypeVar('vtypes', bound=VGeneric)
class Variable(NamedTuple, Generic[vtypes]):
    vtype : vtypes
    value: Any
    validate : callable = None


class ItemSpec(Variable):
    readonly : bool = False

    def __new__(cls, vtype:vtypes=None, value:Any=None, readonly:bool=False):

        if not isinstance(vtype, VGeneric):
            raise ValidationFailed(f"vtype <{type(vtype)}> non valido")
        else:
            print(f"vtype <{type(vtype)}> PASSED")

        result, _v, msg = attach_validator(vtype)
        if not result:
            raise ValidationFailed(msg)
        
        value = _v(value) 
        if type(value) is ValidationFailed:
            raise ValidationFailed(f'validation failed: {value}')
        
        instance = super().__new__(cls, vtype, value, _v)
        instance.readonly = readonly

        return instance