from ansible import __version__
from ansible.errors import AnsibleError
from distutils.version import LooseVersion
from operator import eq, ge, gt
from platform import python_version, python_version_tuple

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

version_requirement = '2.10.0'
version_tested_max = '5.4.0'

if python_version_tuple()[0] == '2':
    raise AnsibleError(('Trellis no longer supports Python 2 (you are using version {}).'
                        ' Python 2 reached end of life in 2020 and is unmaintained.\n'
                        'Python 3 is required as of Trellis version v1.15.0.').format(python_version()))

if not ge(LooseVersion(__version__), LooseVersion(version_requirement)):
    raise AnsibleError(('Trellis no longer supports Ansible {}.\n'
        'Please upgrade to Ansible {} or higher.').format(__version__, version_requirement))
elif gt(LooseVersion(__version__), LooseVersion(version_tested_max)):
    display.warning(u'Your Ansible version is {} but this version of Trellis has only been tested for '
            u'compatability with Ansible {} -> {}. It is advisable to check for Trellis updates or '
            u'downgrade your Ansible version.'.format(__version__, version_requirement, version_tested_max))

# Import BaseVarsPlugin after Ansible version check.
# Otherwise import error for Ansible versions older than 2.4 would prevent display of version check message.
from ansible.plugins.vars import BaseVarsPlugin


class VarsModule(BaseVarsPlugin):

    def get_vars(self, loader, path, entities, cache=True):
        return {}
