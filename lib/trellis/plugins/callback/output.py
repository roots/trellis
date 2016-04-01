# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os.path
import sys

from ansible.plugins.callback.default import CallbackModule as CallbackModule_default

try:
    from trellis.utils.output import display_output
except ImportError:
    if sys.path.append(os.path.join(os.getcwd(), 'lib')) in sys.path: raise
    sys.path.append(sys.path.append(os.path.join(os.getcwd(), 'lib')))
    from trellis.utils.output import display_output


class CallbackModule(CallbackModule_default):
    ''' Customizes the default Ansible output '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'output'

    def __init__(self):

        super(CallbackModule, self).__init__()

        self.action = None
        self.first_host = True
        self.first_item = True
        self.task_failed = False

    def display_host_output(self, result):
        if 'results' not in result._result:
            display_output(result, self.action, self._display.display, self.first_host and self.first_item, self.task_failed)
            self.first_host = False

    def display_item_output(self, result):
        display_output(result, self.action, self._display.display, self.first_host and self.first_item, self.task_failed)
        self.first_item = False

    def reset_task(self, task):
        self.action = task._get_parent_attribute('action')
        self.first_host = True
        self.first_item = True
        self.task_failed = False

    # Display dict key only, instead of full json dump
    def replace_item_with_key(self, result):
        if not self._display.verbosity:
            if 'key' in result._result['item']:
                result._result['item'] = result._result['item']['key']
            elif 'item' in result._result['item'] and 'key' in result._result['item']['item']:
                result._result['item'] = result._result['item']['item']['key']

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.task_failed = True
        self.display_host_output(result)
        super(CallbackModule, self).v2_runner_on_failed(result, ignore_errors)

    def v2_runner_on_ok(self, result):
        self.display_host_output(result)
        super(CallbackModule, self).v2_runner_on_ok(result)

    def v2_runner_on_skipped(self, result):
        self.display_host_output(result)
        super(CallbackModule, self).v2_runner_on_skipped(result)

    def v2_runner_on_unreachable(self, result):
        self.task_failed = True
        self.display_host_output(result)
        super(CallbackModule, self).v2_runner_on_unreachable(result)

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.reset_task(task)
        super(CallbackModule, self).v2_playbook_on_task_start(task, is_conditional)

    def v2_playbook_on_handler_task_start(self, task):
        self.reset_task(task)
        super(CallbackModule, self).v2_playbook_on_handler_task_start(task)

    def v2_playbook_item_on_ok(self, result):
        self.display_item_output(result)
        self.replace_item_with_key(result)
        super(CallbackModule, self).v2_playbook_item_on_ok(result)

    def v2_playbook_item_on_failed(self, result):
        self.task_failed = True
        self.display_item_output(result)
        self.replace_item_with_key(result)
        super(CallbackModule, self).v2_playbook_item_on_failed(result)

    def v2_playbook_item_on_skipped(self, result):
        self.display_item_output(result)
        self.replace_item_with_key(result)
        super(CallbackModule, self).v2_playbook_item_on_skipped(result)
