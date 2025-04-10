import platform
from functools import partial, singledispatch
from pathlib import Path #, WindowsPath, PosixPath
from pathvalidate import is_valid_filename, is_valid_filepath

_PLATFORM_  = platform.system()

from vtypes import(
    VString, VPath
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


def _path_validator(_value, type=Path, cast=True, exist=None):
    # vedi anche : 
    # https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta#34102855
    # ISSUE #64
    
    _stripped   = str(_value).strip()
    try:
        if is_valid_filepath(_stripped, platform=_PLATFORM_):
            _value = type(_value)           
            if exist :
                # eager path
                _value.mkdir(parents=True, exist_ok=False) # raise FileExistsError if already exists
                #_created = True
            else:
                # lazy path
                return _value
        else:
            # invalid path
            return ValidationFailed(f'INVALID PATH PASSED : <{_stripped}>') # test        
        '''if _created:
            print(f'PATH <{_stripped}> CREATED')'''
        
        return _value
        
    except FileExistsError:
        return _value 
    except ValueError as e:
        return ValidationFailed(f'<{e}> (ValueError)')
    except FileNotFoundError as e:
        return ValidationFailed(f'<{e}> (FileNotFoundError)')
    except PermissionError as e : # ISSUE #65
        return ValidationFailed(f'<{e}> (PermissionError)')

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
    
@attach_validator.register(VPath)
def _(candidate):
    msg = ''
    try:
        _v = partial(_path_validator,
                    type=candidate.type,
                    cast=candidate.cast,
                    exist=candidate.exist)
        return True, _v, msg
    except Exception as e:          
        msg += f'<WRONG VALIDATOR> {e} '
        return False, None, msg
