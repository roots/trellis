# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function, unicode_literals)
__metaclass__ = type

import types

try:
    import json
except ImportError:
    import simplejson as json

from ansible import errors
from ansible.compat.six import string_types
from ansible.module_utils.urls import open_url

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
                try:
                    url = 'https://tldextract.appspot.com/api/extract?url={0}'.format(host)
                    data = json.load(open_url(url, timeout=5))
                    subdomain = data.get('subdomain', '')
                except IOError:
                    subdomain = ''

                if subdomain != '':
                    return host

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
