# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import textwrap

from ansible.utils.unicode import to_unicode

def display_output(result, action, display, first, task_failed=False):
    msg = ''
    result = result._result
    wrap_width = 77
    failed = 'failed' in result or 'unreachable' in result

    # Only display msg if debug module or if failed (some modules have undesired 'msg' on 'ok')
    if 'msg' in result and (failed or action == 'debug'):
        msg = result.pop('msg', '')

        # Disable Ansible's verbose setting for debug module to avoid the CallbackBase._dump_results()
        if '_ansible_verbose_always' in result:
            del result['_ansible_verbose_always']

    # Display additional info when failed
    if failed:
        items = (item for item in ['module_stderr', 'module_stdout', 'stderr'] if item in result and to_unicode(result[item]) != '')
        for item in items:
            msg = result[item] if msg == '' else '\n'.join([msg, result.pop(item, '')])

        # Add blank line between this fail message and the json dump Ansible displays next
        msg = '\n'.join([msg, ''])

    # Must pass unicode strings to Display.display() to prevent UnicodeError tracebacks
    if isinstance(msg, list):
        msg = '\n'.join([to_unicode(x) for x in msg])
    elif not isinstance(msg, unicode):
        msg = to_unicode(msg)

    # Wrap text
    msg = '\n'.join([textwrap.fill(line, wrap_width, replace_whitespace=False)
                     for line in msg.splitlines()])

    # Display msg with horizontal rule between hosts/items
    hr = '-' * int(wrap_width*.67)
    if msg == '':
        if task_failed and not first:
            display(hr, 'bright gray')
        else:
            return
    else:
        if not first:
            display(hr, 'bright gray')
        display(msg, 'red' if failed else 'bright purple')
