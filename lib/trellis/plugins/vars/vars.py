from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

from ansible import __version__
from ansible.errors import AnsibleError

if __version__.startswith('1'):
    raise AnsibleError('Trellis no longer supports Ansible 1.x. Please upgrade to Ansible 2.x.')

# These imports will produce Traceback in Ansible 1.x, so place after version check
from __main__ import cli
from ansible.compat.six import iteritems
from ansible.parsing.yaml.objects import AnsibleMapping, AnsibleSequence, AnsibleUnicode


class VarsModule(object):
    ''' Creates and modifies host variables '''

    def __init__(self, inventory):
        self.inventory = inventory
        self.inventory_basedir = inventory.basedir()
        self._options = cli.options if cli else None

    def raw_triage(self, key_string, item, patterns):
        # process dict values
        if isinstance(item, AnsibleMapping):
            dict = {}
            for key,value in item.iteritems():
                dict[key] = self.raw_triage('.'.join([key_string, key]), value, patterns)
            return dict

        # process list values
        elif isinstance(item, AnsibleSequence):
            list = []
            for i,value in enumerate(item):
                raw = self.raw_triage('.'.join([key_string, str(i)]), value, patterns)
                list.append(raw)
            return list

        # wrap values if they match raw_vars pattern
        elif isinstance(item, AnsibleUnicode):
            matches = False
            for pattern in patterns:
                if re.match(pattern, key_string) is not None:
                    matches = True
                    break

            if not item.startswith(('{% raw', '{%raw')) and matches:
                item = ''.join(['{% raw %}', item, '{% endraw %}'])

            return item

    def raw_vars(self, host, hostvars):
        if 'raw_vars' not in hostvars:
            return

        raw_vars = list((var for var in hostvars['raw_vars'] if var.split('.')[0] in hostvars))

        # prepare regex match patterns
        patterns = []
        for pattern in raw_vars:
            pattern = re.sub(r'\.', '\.', pattern)
            pattern = re.sub(r'\*', '(.)*', pattern)
            patterns.append(pattern)

        # wrap matching vars under each key
        keys = set()
        for var in raw_vars:
            key = var.split('.')[0]
            if key in keys:
                continue

            host.vars[key] = self.raw_triage(key, hostvars[key], patterns)
            keys.add(key)

    def cli_options(self):
        options = []

        strings = {
            '--connection': 'connection',
            '--inventory-file': 'inventory',
            '--private-key': 'private_key_file',
            '--ssh-common-args': 'ssh_common_args',
            '--ssh-extra-args': 'ssh_extra_args',
            '--timeout': 'timeout',
            '--vault-password-file': 'vault_password_file',
            }

        for option,value in strings.iteritems():
            if getattr(self._options, value, False):
                options.append("{0}='{1}'".format(option, str(getattr(self._options, value))))

        if getattr(self._options, 'ask_vault_pass', False):
            options.append('--ask-vault-pass')

        return ' '.join(options)

    def get_host_vars(self, host, vault_password=None):
        self.raw_vars(host, host.get_group_vars())
        host.vars['cli_options'] = self.cli_options()
        host.vars['cli_ask_pass'] = getattr(self._options, 'ask_pass', False)
        return {}
