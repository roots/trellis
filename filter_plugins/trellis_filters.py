# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import types

from ansible import errors
from ansible.compat.six import string_types

def reverse_www(value):
    ''' Add or remove www subdomain '''

    # Check if value is a list and parse each item
    if isinstance(value, (list, tuple, types.GeneratorType)):
        values = []
        for item in value:
            values.append(reverse_www(item))
        return values

    # Add or remove www
    elif isinstance(value, string_types):
        if value.startswith('www.'):
            return value[4:]
        else:
            return 'www.{0}'.format(value)

    # Handle invalid input type
    else:
        raise errors.AnsibleFilterError('The reverse_www filter expects a string or list of strings, got ' + repr(value))


class FilterModule(object):
    ''' Trellis jinja2 filters '''

    def filters(self):
        return {
            'reverse_www': reverse_www,
        }
