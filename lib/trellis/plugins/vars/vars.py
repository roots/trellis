from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re
import sys

from ansible import __version__
from ansible.errors import AnsibleError

if __version__.startswith('1'):
    raise AnsibleError('Trellis no longer supports Ansible 1.x. Please upgrade to Ansible 2.x.')

# These imports will produce Traceback in Ansible 1.x, so place after version check
from __main__ import cli
from ansible.compat.six import iteritems
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.yaml.objects import AnsibleMapping, AnsibleSequence, AnsibleUnicode
from ansible.template import Templar


class VarsModule(object):
    ''' Creates and modifies host variables '''

    def __init__(self, inventory):
        self.inventory = inventory
        self.inventory_basedir = inventory.basedir()
        self.loader = DataLoader()
        self._options = cli.options if cli else None

    def raw_triage(self, key_string, item, patterns):
        # process dict values
        if isinstance(item, AnsibleMapping):
            return dict((key,self.raw_triage('.'.join([key_string, key]), value, patterns)) for key,value in item.iteritems())

        # process list values
        elif isinstance(item, AnsibleSequence):
            return [self.raw_triage('.'.join([key_string, str(i)]), value, patterns) for i,value in enumerate(item)]

        # wrap values if they match raw_vars pattern
        elif isinstance(item, AnsibleUnicode):
            match = next((pattern for pattern in patterns if re.match(pattern, key_string)), None)
            return ''.join(['{% raw %}', item, '{% endraw %}']) if not item.startswith(('{% raw', '{%raw')) and match else item

    def raw_vars(self, host, hostvars):
        if 'raw_vars' not in hostvars:
            return

        raw_vars = Templar(variables=hostvars, loader=self.loader).template(hostvars['raw_vars'])
        if not isinstance(raw_vars, list):
            raise AnsibleError('The `raw_vars` variable must be defined as a list.')

        patterns = [re.sub(r'\*', '(.)*', re.sub(r'\.', '\.', var)) for var in raw_vars if var.split('.')[0] in hostvars]
        keys = set(pattern.split('\.')[0] for pattern in patterns)
        for key in keys:
            host.vars[key] = self.raw_triage(key, hostvars[key], patterns)

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

    def darwin_without_passlib(self):
        if not sys.platform.startswith('darwin'):
            return False

        try:
            import passlib.hash
            return False
        except:
            return True

    def get_host_vars(self, host, vault_password=None):
        self.raw_vars(host, host.get_group_vars())
        host.vars['cli_options'] = self.cli_options()
        host.vars['cli_ask_pass'] = getattr(self._options, 'ask_pass', False)
        host.vars['cli_ask_become_pass'] = getattr(self._options, 'become_ask_pass', False)
        host.vars['darwin_without_passlib'] = self.darwin_without_passlib()
        return {}
