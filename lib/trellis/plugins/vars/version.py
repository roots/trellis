# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import __version__
from ansible.errors import AnsibleError
from distutils.version import LooseVersion
from operator import ge

version_requirement = '2.2.0.0'
if not ge(LooseVersion(__version__), LooseVersion(version_requirement)):
    raise AnsibleError(('Trellis no longer supports Ansible {}.\n'
        'Please upgrade to Ansible {} or higher.').format(__version__, version_requirement))


class VarsModule(object):
    ''' Creates and modifies host variables '''

    def __init__(self, inventory):
        pass
