from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import __version__
from ansible.errors import AnsibleError

if __version__.startswith('1'):
    raise AnsibleError('Trellis no longer supports Ansible 1.x. Please upgrade to Ansible 2.x.')

# This import will produce Traceback in Ansible 1.x, so place after version check
from __main__ import cli


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

    def cli_args_vault(self):
        if self._options.ask_vault_pass:
            return '--ask-vault-pass'
        elif self._options.vault_password_file:
            return '--vault-password-file {0}'.format(self._options.vault_password_file)
        else:
            return ''

    def get_host_vars(self, host, vault_password=None):
        self.wrap_salts_in_raw(host, host.get_group_vars())
        host.vars['cli_args_vault'] = self.cli_args_vault()
        return {}
