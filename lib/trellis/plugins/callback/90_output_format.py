# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os.path
import platform
import re
import sys
import textwrap

from ansible import __version__
from ansible import constants as C
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.callback import CallbackBase
from ansible.utils.color import codeCodes, stringc
from ansible.utils.unicode import to_unicode

try:
    from trellis.plugins.callback import TrellisCallbackBase
except ImportError:
    if sys.path.append(os.path.join(os.getcwd(), 'lib')) in sys.path: raise
    sys.path.append(sys.path.append(os.path.join(os.getcwd(), 'lib')))
    from trellis.plugins.callback import TrellisCallbackBase

# Retain these constants' definitions until min required Ansible version includes...
# https://github.com/bcoca/ansible/commit/d3deb24#diff-b77962b6b54a830ec373de0602918318R271
C.COLOR_SKIP = C.get_config(C.p, 'colors', 'skip', 'ANSIBLE_COLOR_SKIP', 'cyan')
C.COLOR_ERROR = C.get_config(C.p, 'colors', 'error', 'ANSIBLE_COLOR_ERROR', 'red')
C.COLOR_WARN = C.get_config(C.p, 'colors', 'warn', 'ANSIBLE_COLOR_WARN', 'bright purple')
C.COLOR_CHANGED = C.get_config(C.p, 'colors', 'ok', 'ANSIBLE_COLOR_CHANGED', 'yellow')
C.COLOR_OK = C.get_config(C.p, 'colors', 'ok', 'ANSIBLE_COLOR_OK', 'green')


class CallbackModule(TrellisCallbackBase, CallbackBase):
    ''' Displays Ansible output and custom messages in readable format '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'output_format'

    def __init__(self):

        super(CallbackModule, self).__init__()

        # Configs manually defined here
        self.header_fail = '  Trellis Debug'
        self.output_docs = 'To manage this output, see https://roots.io/trellis/docs/cli-output/'

        # Auto-populated variables
        self.disabled = False
        self.error_task = None
        self.error_msg = []
        self.vagrant_version = None

        # Optional configs from trellis.cfg
        self.colorize_code = C.get_config(self.cfg, 'output_custom', 'colorize_code', 'TRELLIS_COLORIZE_CODE', True, boolean=True)
        self.color_default = C.get_config(self.cfg, 'output_custom', 'color_default', 'TRELLIS_COLOR_DEFAULT', C.COLOR_SKIP)
        self.color_ok = C.get_config(self.cfg, 'output_custom', 'color_ok', 'TRELLIS_COLOR_OK', C.COLOR_OK)
        self.color_error = C.get_config(self.cfg, 'output_custom', 'color_error', 'TRELLIS_COLOR_ERROR', C.COLOR_ERROR)
        self.color_warn = C.get_config(self.cfg, 'output_custom', 'color_warn', 'TRELLIS_COLOR_WARN', C.COLOR_WARN)
        self.color_code = C.get_config(self.cfg, 'output_custom', 'color_code', 'TRELLIS_COLOR_CODE', 'normal')
        self.color_code_block = C.get_config(self.cfg, 'output_custom', 'color_code_block', 'TRELLIS_COLOR_CODE_BLOCK', C.COLOR_CHANGED)
        self.color_hr = C.get_config(self.cfg, 'output_custom', 'color_hr', 'TRELLIS_COLOR_HR', 'bright gray')
        self.color_footer = C.get_config(self.cfg, 'output_custom', 'color_footer', 'TRELLIS_COLOR_FOOTER', 'bright gray')

    def system(self):
        vagrant = ' Vagrant {0};'.format(self.vagrant_version) if self.vagrant_version else ''
        return 'Ansible {0};{1} {2}'.format(__version__, vagrant, platform.system())

    # Get most recent CHANGELOG entry
    def changelog_msg(self):
        changelog_msg = ''
        changelog = os.path.join(os.getcwd(), 'CHANGELOG.md')

        if os.path.isfile(changelog):
            with open(changelog) as f:
                str = f.read(200)

            # Retrieve release number if it is most recent entry
            release = re.search(r'^###\s((?!HEAD).*)', str)
            if release is not None:
                changelog_msg = 'Trellis {0}'.format(release.group(1))

            # Retrieve most recent changelog entry
            else:
                change = re.search(r'.*\n\*\s*([^\(\n\[]+)', str)
                if change is not None:
                    changelog_msg = 'Trellis at "{0}"'.format(change.group(1).strip())

        return changelog_msg

    def wrap(self, chunk):
        # Extract ANSI escape codes
        pattern = r'(\033\[.*?m|\033\[0m)'
        codes = re.findall(pattern, chunk)

        # Achieve more accurate wrap width by replacing multi-character ANSI escape codes with single character placeholder
        sub = None
        sub_candidates = ['~', '^', '|', '#', '@', '$', '&', '*', '?', '!', ';', '+', '=', '<', '>', '%', '-', '9', '8']
        for candidate in sub_candidates:
            if candidate not in chunk:
                sub = candidate
                break
        chunk = re.sub(pattern, sub, chunk)

        # Wrap text
        chunk = '\n'.join([textwrap.fill(line, self.wrap_width, replace_whitespace=False)
                           for line in chunk.splitlines()])

        # Replace placeholders with original ANSI escape codes
        for code in codes:
            chunk = chunk.replace(sub, code, 1)

        return chunk

    def colorize_defaults(self, chunk, color):
        if 'C_ERROR' in chunk:
            chunk = self.split_and_colorize(chunk, color, 'C_ERROR', self.color_error)
        elif 'C_OK' in chunk:
            chunk = self.split_and_colorize(chunk, color, 'C_OK', self.color_ok)
        elif 'C_WARN' in chunk:
            chunk = self.split_and_colorize(chunk, color, 'C_WARN', self.color_warn)
        elif 'C_BOLD' in chunk:
            color_bold = color
            if not color.startswith(('black', 'normal', 'white', 'bright')):
                color_bold = 'bright {0}'.format(color)
            elif color == 'dark gray':
                color_bold = 'bright gray'
            chunk = self.split_and_colorize(chunk, color, 'C_BOLD', color_bold)
        else:
            chunk = stringc(chunk, color)

        return chunk

    def split_and_colorize(self, chunk, color_1, sep=None, color_2=None):
        if sep is None:
            chunk = self.colorize_defaults(chunk, color_1)
            return chunk

        for n, snippet in enumerate(chunk.split(sep)):
            if n % 2 is 0:
                snippet = self.colorize_defaults(snippet, color_1)
            else:
                snippet = self.colorize_defaults(snippet, color_2)
            chunk = snippet if n is 0 else ''.join([chunk, snippet])

        return chunk

    def get_output(self, result, output=''):
        # Add msgs from looping tasks (e.g., tasks using `with_items`)
        if 'results' in result:
            results = (res for res in result['results'] if 'skipped' not in res)
            for res in results:
                output = self.get_output(res, output)
            return output

        msg = ''
        error = 'failed' in result or 'unreachable' in result

        # Only display msg if debug module or if failed (some modules have undesired 'msg' on 'ok')
        if 'msg' in result and (error or self.action == 'debug'):
            msg = result['msg']

        if 'failed' in result:
            # Display any additional info if available
            for item in ['module_stderr', 'module_stdout', 'stderr']:
                if item in result and to_unicode(result[item]) != '':
                    msg = result[item] if msg == '' else '\n'.join([msg, result[item]])

        # Return original output if nothing to add
        if msg == '':
            return output

        # Choose color
        color = self.color_error if error else self.color_default

        # Convert msg to unicode string because self._diplay.display() can only take strings
        # From ansible/utils/display.py --
        #   "Note: msg *must* be a unicode string to prevent UnicodeError tracebacks."
        if isinstance(msg, list):
            msg = '\n'.join([to_unicode(x) for x in msg])
        elif not isinstance(msg, unicode):
            msg = to_unicode(msg)

        # Apply colors to msg and add textwrap to non-code blocks
        for i, chunk in enumerate(msg.split('\n```\n')):
            if chunk == '':
                continue

            # Non code block text
            if i % 2 is 0:
                # Apply color
                if self.colorize_code:
                    chunk = self.split_and_colorize(chunk.strip(), color, '`', self.color_code)
                else:
                    chunk = self.split_and_colorize(chunk.strip(), color)
                # Apply textwrap
                chunk = self.wrap(chunk)

            # Code block - apply color (no textwrap)
            else:
                chunk = self.split_and_colorize(chunk, self.color_code_block)

            assembled = '\n'.join([chunk, '']) if i is 0 else '\n'.join([assembled, chunk, ''])

        if output != '':
            return '\n'.join([output, assembled]).lstrip()
        else:
            return assembled.lstrip()

    def display_output(self, result):
        output = self.get_output(result._result)

        if output.strip():
            # Prefix output with hostname if multiple hosts
            host_prefix = ''
            if len(self.hosts) > 1 and not self.task_run_once:
                host_prefix = '[{0}]: '.format(result._host.get_name())

            # Save output to display in v2_playbook_on_stats if error, else display now
            if result.is_failed() or result.is_unreachable():
                host_prefix = stringc(host_prefix, self.color_error)
                self.error_msg.append(''.join([host_prefix, output]))
            else:
                host_prefix = stringc(host_prefix, self.color_default)
                self._display.display(''.join([host_prefix, output]))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.error_task = self.task
        self.display_output(result)

    def v2_runner_on_ok(self, result):
        self.display_output(result)

        if not self.display_ok_items and 'results' in result._result:
            for res in result._result['results']:
                if 'item' in res:
                    res['item'] = 'suppressed'

    def v2_runner_on_unreachable(self, result):
        self.display_output(result)

    def v2_playbook_on_handler_task_start(self, task):
        super(CallbackModule, self).v2_playbook_on_handler_task_start(task)

    def v2_playbook_on_play_start(self, play):
        super(CallbackModule, self).v2_playbook_on_play_start(play)
        play.vars['ansible_colors'] = ''.join([stringc(color.ljust(int(self.wrap_width/3)), color)
                                               for color in codeCodes.keys()])
        play.vars['color_settings'] = '\n'.join([
            stringc('color_default: {0}'.format(self.color_default), self.color_default),
            stringc('color_ok: {0}'.format(self.color_ok), self.color_ok),
            stringc('color_error: {0}'.format(self.color_error), self.color_error),
            stringc('color_warn: {0}'.format(self.color_warn), self.color_warn),
            stringc('color_code: {0}'.format(self.color_code if self.colorize_code else
                    '(`colorize_code = False` so no color and `backticks` display)'),
                    self.color_code if self.colorize_code else self.color_default),
            stringc('color_code_block: {0}'.format(self.color_code_block), self.color_code_block),
            stringc('color_hr: {0}'.format(self.color_hr), self.color_hr),
            stringc('color_footer: {0}'.format(self.color_footer), self.color_footer),
            ])

        # Check for relevant settings or overrides passed via cli --extra-vars
        loader = DataLoader()
        play_vars = play.get_variable_manager().get_vars(loader=loader, play=play)

        if 'vagrant_version' in play_vars:
            self.vagrant_version = play_vars['vagrant_version']

        self.disabled = not self.custom_output
        if 'wrap_width' in play_vars:
            self.wrap_width = int(play_vars['wrap_width'])

    def v2_playbook_on_stats(self, stats):
        if self.error_msg:
            # Prepare header
            hr = stringc('-' * self.wrap_width, self.color_hr)
            header = stringc(self.wrap(self.header_fail), self.color_error)
            header = '\n'.join([hr, header, hr])

            if self.error_task is not None:
                error_task = stringc(self.wrap('Error on task "{0}"'.format(self.error_task)), self.color_error)
                header = '\n'.join([header, error_task])

            # Add system info and docs note to footer
            specs = '\n'.join([self.system(), self.changelog_msg()])
            specs = stringc(self.wrap(specs), self.color_footer)
            output_docs = stringc(self.wrap(self.output_docs), self.color_footer)
            hr_small = '-' * min([len(self.system()), self.wrap_width])
            footer = '\n'.join([stringc(hr_small, self.color_hr), specs, output_docs])

            # Add header and footer to error message
            error_msg = '\n'.join(self.error_msg)
            output = '\n'.join(['', header, '', error_msg, footer, hr, '\n'])

            self._display.display(output)
