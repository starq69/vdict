from functools import partial, singledispatch   

from vtypes import(
    VString, 
)

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


@attach_validator.register(VString)
def _(candidate):
    msg = ''
    try:
        _v = partial(_string_validator, options=candidate.options)
        return True, _v, msg
    except Exception as e:   
        msg += f'<WRONG VALIDATOR> {e} '
        return False, None, msg
