from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import __version__
from ansible.errors import AnsibleError

if __version__.startswith('1'):
    raise AnsibleError('Trellis no longer supports Ansible 1.x. Please upgrade to Ansible 2.x.')

# These imports will produce Traceback in Ansible 1.x, so place after version check
from __main__ import cli
from ansible.compat.six import iteritems


class VarsModule(object):
    ''' Creates and modifies host variables '''

    def __init__(self, inventory):
        self.inventory = inventory
        self.inventory_basedir = inventory.basedir()
        self._options = cli.options if cli else None

    # Wrap salts and keys variables in {% raw %} to prevent jinja templating errors
    def wrap_salts_in_raw(self, host, hostvars):
        if 'vault_wordpress_sites' in hostvars:
            for name, site in hostvars['vault_wordpress_sites'].iteritems():
                for key, value in site['env'].iteritems():
                    if key.endswith(('_key', '_salt')) and not value.startswith(('{% raw', '{%raw')):
                        hostvars['vault_wordpress_sites'][name]['env'][key] = ''.join(['{% raw %}', value, '{% endraw %}'])
            host.vars['vault_wordpress_sites'] = hostvars['vault_wordpress_sites']

    def cli_options_ping(self):
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

        booleans = {
            '--ask-pass': 'ask_pass',
            '--ask-vault-pass': 'ask_vault_pass',
            }

        for option,value in booleans.iteritems():
            if getattr(self._options, value, False):
                options.append(option)

        return ' '.join(options)

    def get_host_vars(self, host, vault_password=None):
        self.wrap_salts_in_raw(host, host.get_group_vars())
        host.vars['cli_options_ping'] = self.cli_options_ping()
        return {}
