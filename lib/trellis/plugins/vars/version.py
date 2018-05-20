# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import __version__
from ansible.errors import AnsibleError
from distutils.version import LooseVersion
from operator import eq, ge, gt
from sys import version_info

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

if version_info[0] > 2:
    raise AnsibleError(('Trellis does not yet support Python {}.{}.{}. \n'
        'Please use Python 2.7.').format(version_info[0], version_info[1], version_info[2]))

version_requirement = '2.4.0.0'
version_tested_max = '2.5.3'

if not ge(LooseVersion(__version__), LooseVersion(version_requirement)):
    raise AnsibleError(('Trellis no longer supports Ansible {}.\n'
        'Please upgrade to Ansible {} or higher.').format(__version__, version_requirement))
elif gt(LooseVersion(__version__), LooseVersion(version_tested_max)):
    display.warning(u'You Ansible version is {} but this version of Trellis has only been tested for '
            u'compatability with Ansible {} -> {}. It is advisable to check for Trellis updates or '
            u'downgrade your Ansible version.'.format(__version__, version_requirement, version_tested_max))

if eq(LooseVersion(__version__), LooseVersion('2.5.0')):
    display.warning(u'You Ansible version is {}. Consider upgrading your Ansible version to avoid '
            u'erroneous warnings such as `Removed restricted key from module data...`'.format(__version__))

# Import BaseVarsPlugin after Ansible version check.
# Otherwise import error for Ansible versions older than 2.4 would prevent display of version check message.
from ansible.plugins.vars import BaseVarsPlugin


class VarsModule(BaseVarsPlugin):

    def get_vars(self, loader, path, entities, cache=True):
        return {}
