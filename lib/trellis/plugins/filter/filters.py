# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function, unicode_literals)
__metaclass__ = type

import types

from ansible import errors
from ansible.compat.six import string_types

def reverse_www(hosts, enabled=True, append=True):
    ''' Add or remove www subdomain '''

    if not enabled:
        return hosts

    # Check if hosts is a list and parse each host
    if isinstance(hosts, (list, tuple, types.GeneratorType)):
        reversed_hosts = [reverse_www(host) for host in hosts]

        if append:
            return list(set(hosts + reversed_hosts))
        else:
            return reversed_hosts

    # Add or remove www
    elif isinstance(hosts, string_types):
        host = hosts

        if host.startswith('www.'):
            return host[4:]
        else:
            if len(host.split('.')) > 2:
                return host
            else:
                return 'www.{0}'.format(host)

    # Handle invalid input type
    else:
        raise errors.AnsibleFilterError('The reverse_www filter expects a string or list of strings, got ' + repr(hosts))

def to_env(dict_value):
    envs = ["{0}='{1}'".format(key.upper(), value) for key, value in sorted(dict_value.items())]
    return "\n".join(envs)

def underscore(value):
    ''' Convert dots to underscore in a string '''
    return value.replace('.', '_')

class FilterModule(object):
    ''' Trellis jinja2 filters '''

    def filters(self):
        return {
            'reverse_www': reverse_www,
            'to_env': to_env,
            'underscore': underscore,
        }
