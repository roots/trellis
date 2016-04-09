# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os.path
import sys

from ansible.parsing.dataloader import DataLoader
from ansible.plugins.callback.default import CallbackModule as CallbackModule_default
from ansible.utils.unicode import to_unicode

try:
    from trellis.utils import output as output
except ImportError:
    if sys.path.append(os.path.join(os.getcwd(), 'lib')) in sys.path: raise
    sys.path.append(sys.path.append(os.path.join(os.getcwd(), 'lib')))
    from trellis.utils import output as output


class CallbackModule(CallbackModule_default):
    ''' Customizes the default Ansible output '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'output'

    def __init__(self):
        super(CallbackModule, self).__init__()
        output.load_configs(self)
        output.reset_task_info(self)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.task_failed = True
        output.display_host(self, result)
        super(CallbackModule, self).v2_runner_on_failed(result, ignore_errors)

    def v2_runner_on_ok(self, result):
        output.display_host(self, result)
        super(CallbackModule, self).v2_runner_on_ok(result)

    def v2_runner_on_skipped(self, result):
        output.display_host(self, result)
        super(CallbackModule, self).v2_runner_on_skipped(result)

    def v2_runner_on_unreachable(self, result):
        self.task_failed = True
        output.display_host(self, result)
        super(CallbackModule, self).v2_runner_on_unreachable(result)

    def v2_playbook_on_task_start(self, task, is_conditional):
        output.reset_task_info(self, task)
        if self.display_include_tasks or task._get_parent_attribute('action') != 'include':
            super(CallbackModule, self).v2_playbook_on_task_start(task, is_conditional)

    def v2_playbook_on_handler_task_start(self, task):
        output.reset_task_info(self, task)
        super(CallbackModule, self).v2_playbook_on_handler_task_start(task)

    def v2_playbook_on_play_start(self, play):
        super(CallbackModule, self).v2_playbook_on_play_start(play)

        # Check for relevant settings or overrides passed via cli --extra-vars
        loader = DataLoader()
        play_vars = play.get_variable_manager().get_vars(loader=loader, play=play)
        if 'vagrant_version' in play_vars:
            self.vagrant_version = play_vars['vagrant_version']

    def v2_playbook_on_stats(self, stats):
        super(CallbackModule, self).v2_playbook_on_stats(stats)
        self._display.display('To manage Trellis CLI output, see https://roots.io/trellis/docs/cli-output/\n', 'bright gray')

    def v2_playbook_on_include(self, included_file):
        if self.display_include_tasks:
            super(CallbackModule, self).v2_playbook_on_include(included_file)

    def v2_playbook_item_on_ok(self, result):
        output.display_item(self, result)
        output.replace_item_with_key(self, result)
        output.truncate_item(self, result)
        super(CallbackModule, self).v2_playbook_item_on_ok(result)

    def v2_playbook_item_on_failed(self, result):
        self.task_failed = True
        output.display_item(self, result)
        super(CallbackModule, self).v2_playbook_item_on_failed(result)

    def v2_playbook_item_on_skipped(self, result):
        if self.display_skipped_items:
            output.display_item(self, result)
            output.replace_item_with_key(self, result)
            output.truncate_item(self, result)
            super(CallbackModule, self).v2_playbook_item_on_skipped(result)
