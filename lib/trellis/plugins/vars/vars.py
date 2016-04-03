from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

class VarsModule(object):
    ''' Creates and modifies host variables '''

    def __init__(self, inventory):
        self.inventory = inventory
        self.inventory_basedir = inventory.basedir()

    # Wrap salts and keys variables in {% raw %} to prevent jinja templating errors
    def wrap_salts_in_raw(self, host, hostvars):
        if 'vault_wordpress_sites' in hostvars:
            for name, site in hostvars['vault_wordpress_sites'].iteritems():
                for key, value in site['env'].iteritems():
                    if key.endswith(('_key', '_salt')) and not value.startswith(('{% raw', '{%raw')):
                        hostvars['vault_wordpress_sites'][name]['env'][key] = ''.join(['{% raw %}', value, '{% endraw %}'])
            host.vars['vault_wordpress_sites'] = hostvars['vault_wordpress_sites']

    def get_host_vars(self, host, vault_password=None):
        self.wrap_salts_in_raw(host, host.get_group_vars())
        return {}
