#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket

try:
    from httplib import HTTPConnection, HTTPSConnection, HTTPException
except ImportError:
    # Python 3
    from http.client import HTTPConnection, HTTPSConnection, HTTPException

DOCUMENTATION = '''
---
module: test_challenges
short_description: Tests Let's Encrypt web server challenges
description:
     - The M(test_challenges) module verifies a list of hosts can access acme challenges for Let's Encrypt.
options:
  hosts:
    description:
      - A list of hostnames/domains to test.
    required: true
    default: null
    type: list
  ssl:
    description:
      - If true, will check on SSL port as well.
    required: false
    default: false
    type: bool
  file:
    description:
      - The dummy filename in the URL to test.
    required: no
    default: ping.txt
  path:
    description:
      - The path to the challenges in the URL.
    required: no
    default: /.well-known/acme-challenge
author:
    - Scott Walkinshaw
'''

EXAMPLES = '''
# Example from Ansible Playbooks.
- test_challenges:
    hosts:
      - example.com
      - www.example.com
      - www.mydomain.com
'''

def get_connection(host, port):
    if port == 80:
        conn = HTTPConnection(host, port)
    elif port == 443:
        conn = HTTPSConnection(host, port)
    return conn

def get_status(host, port, path, file):
    uri = '{0}:{1}/{2}/{3}'.format(host,port,path,file)
    request = {
        'hostname': host,
        'uri': uri,
    }

    try:
        conn = get_connection(host, port)
        conn.request('HEAD', '/{0}/{1}'.format(path, file))
        res = conn.getresponse()
    except (HTTPException, socket.timeout, socket.error) as e:
        results = {
            'headers': None,
            'reason': None,
            'status': -1, # a flag indicating failure.
        }
        exception = {
            'exception': str(e),
        }
        return {**request, **results, **exception}

    else:
        results = {
            'status': res.status,
            'headers': res.getheaders(),
            'reason': res.reason,
        }
        return {**request, **results}

def main():
    module = AnsibleModule(
        argument_spec = dict(
            file  = dict(default='ping.txt'),
            hosts = dict(required=True, type='list'),
            ssl = dict(default=False, type='bool'),
            path  = dict(default='.well-known/acme-challenge')
        )
    )

    hosts = module.params['hosts']
    path = module.params['path']
    file = module.params['file']
    ssl = module.params['ssl']

    failed_hosts = []

    for host in hosts:
        result = get_status(host, 80, path, file)
        status = result['status']

        if int(status) != 200 and bool(ssl) == True:
            failed_hosts.append(result)
            # Try again, this time over SSL
            result = get_status(host, 443, path, file)
            status = result['status']

        if int(status) != 200:
            failed_hosts.append(result)

    rc = int(len(failed_hosts) > 0)

    module_result = dict(
        changed=False,
        rc=rc,
        failed_hosts=failed_hosts
    )

    if (rc != 0):
        module.fail_json(msg='Failed to fetch the ACME test file', **module_result)
    else:
        module.exit_json(**module_result)

from ansible.module_utils.basic import *
main()
