# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os.path
import sys

from ansible import constants as C
from ansible.plugins.callback.default import CallbackModule as CallbackModule_default

try:
    from trellis.plugins.callback import TrellisCallbackBase
except ImportError:
    if sys.path.append(os.path.join(os.getcwd(), 'lib')) in sys.path: raise
    sys.path.append(sys.path.append(os.path.join(os.getcwd(), 'lib')))
    from trellis.plugins.callback import TrellisCallbackBase


class CallbackModule(TrellisCallbackBase, CallbackModule_default):
    ''' Suppresses some standard Ansible output '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'output_overrides'

    def __init__(self):

        super(CallbackModule, self).__init__()

        # Optional configs from trellis.cfg
        self.display_skipped_items = C.get_config(self.cfg, 'output_general', 'display_skipped_items', 'TRELLIS_DISPLAY_SKIPPED_ITEMS', False, boolean=True)
        self.display_include_tasks = C.get_config(self.cfg, 'output_general', 'display_include_tasks', 'TRELLIS_DISPLAY_INCLUDE_TASKS', False, boolean=True)

    def suppress_output(self, result):
        return (self.custom_output and self._display.verbosity < 3 and (
               (self.action in ['debug', 'fail'] and 'msg' in result._result) or
               ('failed' in result._result and self.action in ['assert', 'setup'])))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        if not self.suppress_output(result):
            super(CallbackModule, self).v2_runner_on_failed(result, ignore_errors)

    def v2_runner_on_ok(self, result):
        if not self.suppress_output(result):
            super(CallbackModule, self).v2_runner_on_ok(result)

    def v2_runner_on_unreachable(self, result):
        if not self.suppress_output(result):
            super(CallbackModule, self).v2_runner_on_unreachable(result)

    def v2_playbook_on_task_start(self, task, is_conditional):
        if self.display_include_tasks or task._get_parent_attribute('action') != 'include' or self._display.verbosity > 2:
            super(CallbackModule, self).v2_playbook_on_task_start(task, is_conditional)

    def v2_playbook_on_include(self, included_file):
        if self.display_include_tasks or self._display.verbosity > 2:
            super(CallbackModule, self).v2_playbook_on_include(included_file)

    def v2_playbook_item_on_ok(self, result):
        if not self.suppress_output(result):
            super(CallbackModule, self).v2_playbook_item_on_ok(result)

    def v2_playbook_item_on_failed(self, result):
        if not self.suppress_output(result):
            super(CallbackModule, self).v2_playbook_item_on_failed(result)

    def v2_playbook_item_on_skipped(self, result):
        if (self.display_skipped_items or self._display.verbosity > 2) and not self.suppress_output(result):
            super(CallbackModule, self).v2_playbook_item_on_skipped(result)
