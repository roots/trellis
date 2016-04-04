# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os.path
import platform
import re
import textwrap

from ansible import __version__
from ansible.utils.unicode import to_unicode

def system(vagrant_version=None):
    # Get most recent Trellis CHANGELOG entry
    changelog_msg = ''
    changelog = os.path.join(os.getcwd(), 'CHANGELOG.md')

    if os.path.isfile(changelog):
        with open(changelog) as f:
            str = f.read(200)

        # Retrieve release number if it is most recent entry
        release = re.search(r'^###\s((?!HEAD).*)', str)
        if release is not None:
            changelog_msg = '\n  Trellis {0}'.format(release.group(1))

        # Retrieve most recent changelog entry
        else:
            change = re.search(r'.*\n\*\s*([^\(\n\[]+)', str)
            if change is not None:
                changelog_msg = '\n  Trellis at "{0}"'.format(change.group(1).strip())

    # Vagrant info, if available
    vagrant = ' Vagrant {0};'.format(vagrant_version) if vagrant_version else ''

    # Assemble components and return
    return 'System info:\n  Ansible {0};{1} {2}{3}'.format(__version__, vagrant, platform.system(), changelog_msg)

def display_output(result, action, display, first, task_failed=False, vagrant_version=None):
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

    # Display system info and msg, with horizontal rule between hosts/items
    hr = '-' * int(wrap_width*.67)

    if task_failed and first:
        display(system(vagrant_version), 'bright gray')
        display(hr, 'bright gray')

    if msg == '':
        if task_failed and not first:
            display(hr, 'bright gray')
        else:
            return
    else:
        if not first:
            display(hr, 'bright gray')
        display(msg, 'red' if failed else 'bright purple')
