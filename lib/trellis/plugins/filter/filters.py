import types

from ansible import errors
from ansible.module_utils.six import string_types
from jinja2 import pass_environment

def to_env(dict_value):
    envs = ['{0}="{1}"'.format(key.upper(), str(value).replace('"', '\\"')) for key, value in sorted(dict_value.items())]
    return "\n".join(envs)

def underscore(value):
    ''' Convert dots to underscore in a string '''
    return value.replace('.', '_')

def php_extensions(value, php_version, package_state):
    """Normalize php_extensions_custom into a dict.

    Accepts either a dict (passed through unchanged for back-compat) or a
    list of short names. Each short name is expanded to
    "php<version>-<name>": "<package_state>".
    """
    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        return {f"php{php_version}-{name}": package_state for name in value}
    return {}

def get_nested_attr(data, attr_path):
    """Helper to safely get a nested attribute from a dict."""
    keys = attr_path.split('.')
    for key in keys:
        if not isinstance(data, dict) or key not in data:
            return None
        data = data[key]
    return data

@pass_environment
def select_sites(env, sites, attr_path, test_name='defined', *args):
    """
    A filter that mimics selectattr but works on nested attributes safely.
    It uses Jinja's own built-in tests.
    """
    test_func = env.tests.get(test_name)
    if test_func is None:
        raise Exception(f"Unknown Jinja2 test '{test_name}'")

    if not isinstance(sites, dict):
        return {}

    result = {}
    for name, site_data in sites.items():
        value_to_test = get_nested_attr(site_data, attr_path)

        # For most tests, we skip sites where the attribute doesn't exist.
        if value_to_test is None and test_name != 'defined':
            continue

        # Handle tests that don't take arguments, like 'true' or 'false'
        if not args and test_name in ['true', 'false', 'undefined', 'defined']:
             if test_func(value_to_test):
                result[name] = site_data
        # Handle tests that do take arguments
        elif test_func(value_to_test, *args):
            result[name] = site_data

    return result

class FilterModule(object):
    def filters(self):
        return {
            'select_sites': select_sites,
            'to_env': to_env,
            'underscore': underscore,
            'php_extensions': php_extensions,
        }
