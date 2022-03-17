import types

from ansible import errors
from ansible.module_utils.six import string_types

def to_env(dict_value):
    envs = ["{0}='{1}'".format(key.upper(), str(value).replace("'","\\'")) for key, value in sorted(dict_value.items())]
    return "\n".join(envs)

def underscore(value):
    ''' Convert dots to underscore in a string '''
    return value.replace('.', '_')

class FilterModule(object):
    ''' Trellis jinja2 filters '''

    def filters(self):
        return {
            'to_env': to_env,
            'underscore': underscore,
        }
