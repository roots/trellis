# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os.path
import sys

DOCUMENTATION = '''
    callback: output
    type: stdout
    short_description: Custom output for Trellis
    extends_documentation_fragment:
      - default_callback
'''

from ansible.plugins.callback.default import CallbackModule as CallbackModule_default

try:
    from trellis.utils import output as output
except ImportError:
    ansible_config_path = os.getenv('ANSIBLE_CONFIG')
    ansible_path = os.path.dirname(ansible_config_path) if ansible_config_path else os.getcwd()
    if sys.path.append(os.path.join(ansible_path, 'lib')) in sys.path: raise
    sys.path.append(sys.path.append(os.path.join(ansible_path, 'lib')))
    from trellis.utils import output as output


class CallbackModule(CallbackModule_default):
    ''' Customizes the default Ansible output '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'output'

    def __init__(self):
        super(CallbackModule, self).__init__()
        output.reset_task_info(self)
        self.vagrant_version = None

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
        super(CallbackModule, self).v2_playbook_on_task_start(task, is_conditional)

    def v2_playbook_on_handler_task_start(self, task):
        output.reset_task_info(self, task)
        super(CallbackModule, self).v2_playbook_on_handler_task_start(task)

    def v2_playbook_on_play_start(self, play):
        super(CallbackModule, self).v2_playbook_on_play_start(play)

        # Check for relevant settings or overrides passed via cli --extra-vars
        extra_vars = play.get_variable_manager().extra_vars
        if 'vagrant_version' in extra_vars:
            self.vagrant_version = extra_vars['vagrant_version']

    def v2_runner_item_on_ok(self, result):
        output.display_item(self, result)
        output.replace_item_with_key(self, result)
        super(CallbackModule, self).v2_runner_item_on_ok(result)

    def v2_runner_item_on_failed(self, result):
        self.task_failed = True
        output.display_item(self, result)
        output.replace_item_with_key(self, result)
        super(CallbackModule, self).v2_runner_item_on_failed(result)

    def v2_runner_item_on_skipped(self, result):
        output.display_item(self, result)
        output.replace_item_with_key(self, result)
        super(CallbackModule, self).v2_runner_item_on_skipped(result)
