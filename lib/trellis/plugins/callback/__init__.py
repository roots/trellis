# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os.path

from __main__ import cli

from ansible import constants as C
from ansible.compat.six import iteritems
from ansible.compat.six.moves import configparser
from ansible.errors import AnsibleOptionsError
from ansible.parsing.dataloader import DataLoader
from ansible.utils.unicode import to_unicode


class TrellisCallbackBase:
    ''' Common attributes and methods for Trellis callback plugins '''

    def __init__(self):

        super(TrellisCallbackBase, self).__init__()

        if cli:
            self._options = cli.options
        else:
            self._options = None

        # Optional configs from trellis.cfg
        self.cfg = self.load_config()
        self.custom_output = C.get_config(self.cfg, 'output_custom', 'custom_output', 'TRELLIS_CUSTOM_OUTPUT', True, boolean=True)
        self.display_ok_items = C.get_config(self.cfg, 'output_custom', 'display_ok_items', 'TRELLIS_DISPLAY_OK_ITEMS', False, boolean=True)
        self.wrap_width = int(C.get_config(self.cfg, 'output_custom', 'wrap_width', 'TRELLIS_WRAP_WIDTH', 77))

        # Auto-populated variables
        self.disabled = False
        self.hosts = set()
        self.task = None
        self.task_run_once = False
        self.action = None

    def load_config(self):
        p = configparser.ConfigParser()
        try:
            p.read(os.path.join(os.getcwd(), 'trellis.cfg'))
        except configparser.Error as e:
            raise AnsibleOptionsError("Error reading config file: \n{0}".format(e))
        return p

    def load_task_info(self, task):
        self.task = task.get_name()
        self.task_run_once = task._get_parent_attribute('run_once')
        self.action = task._get_parent_attribute('action')

    def wrap_salts_in_raw(self, hostvars):
        if 'vault_wordpress_sites' in hostvars:
            for name, site in hostvars['vault_wordpress_sites'].iteritems():
                for key, value in site['env'].iteritems():
                    if key.endswith(('_key', '_salt')) and not value.startswith(('{% raw', '{%raw')):
                        hostvars['vault_wordpress_sites'][name]['env'][key] = ''.join(['{% raw %}', value, '{% endraw %}'])

    def v2_playbook_on_task_start(self, task, is_conditional):
        super(TrellisCallbackBase, self).v2_playbook_on_task_start(task, is_conditional)
        self.load_task_info(task)

    def v2_playbook_on_handler_task_start(self, task):
        super(TrellisCallbackBase, self).v2_playbook_on_handler_task_start(task)
        self.load_task_info(task)

    def v2_playbook_on_play_start(self, play):
        super(TrellisCallbackBase, self).v2_playbook_on_play_start(play)
        loader = DataLoader()
        play_vars = play.get_variable_manager().get_vars(loader=loader, play=play)

        # Check for settings overrides passed via cli --extra-vars
        if 'custom_output' in play_vars:
            self.custom_output = play_vars['custom_output'].lower() != 'false'

        env = 'development' if 'env' not in play_vars else play_vars['env']
        hosts_env_group = [host.name for host in play.get_variable_manager()._inventory.list_hosts(env)]

        # Future additions to TrellisCallbackBase will expand on this loop through hosts and their vars
        hosts = (host for host in play.get_variable_manager()._inventory.get_hosts() if to_unicode(host) in hosts_env_group)
        for host in hosts:
            hostname = host.get_name()
            self.hosts.add(hostname)

            # Wrap salts and keys variables in {% raw %} to prevent jinja templating errors
            vars = {}
            vars[hostname] = play.get_variable_manager().get_vars(loader=loader, play=play, host=host)
            self.wrap_salts_in_raw(vars[hostname])
