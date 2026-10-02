"""Regression tests for the raw_vars callback plugin.

raw_vars keeps matching values out of Ansible's templating so a literal `{{`
in a vault value does not blow up a deploy. These tests assert the behavior
rather than the wrapper type, since the type differs between Ansible versions.
"""

import re

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

from trellis.plugins.callback.vars import CallbackModule

try:
    # ansible-core >= 2.18 tags loaded strings as trusted for templating.
    from ansible.template import trust_as_template
except ImportError:  # pragma: no cover - compatibility for older Ansible versions
    def trust_as_template(value: str) -> str:
        return value


SITE_VARS = """\
vault_wordpress_sites:
  example.com:
    env:
      DB_PASSWORD: "{{ db_password }}literal{{ more }}"
      DB_HOST: "{{ db_host }}"
      AUTH_KEYS:
        - "{{ first_key }}"
        - "{{ second_key }}"
      DB_PORT: 3306
      DISABLE_WP_CRON: true
vault_users:
  admin:
    password: "{{ admin_password }}"
"""


def load_site_vars():
    """Load vars the way Ansible loads host/group vars, so values carry trust."""
    return DataLoader().load(trust_as_template(SITE_VARS))


def raw_var_patterns(raw_vars):
    """Mirror the regex build in CallbackModule.raw_vars."""
    return [re.sub(r"\*", "(.)*", re.sub(r"\.", r"\.", var)) for var in raw_vars]


def triage(raw_vars, key):
    data = load_site_vars()
    # __init__ reads context.CLIARGS, which is absent outside a real play.
    module = CallbackModule.__new__(CallbackModule)
    return module.raw_triage(key, data[key], raw_var_patterns(raw_vars))


def template(value, **variables):
    return Templar(loader=DataLoader(), variables=variables).template(value)


def test_matching_nested_value_is_left_untemplated():
    result = triage(["vault_wordpress_sites"], "vault_wordpress_sites")

    value = result["example.com"]["env"]["DB_PASSWORD"]

    assert template(value, db_password="leaked", more="leaked") == "{{ db_password }}literal{{ more }}"


def test_non_matching_nested_value_is_still_templated():
    result = triage(["vault_wordpress_sites.*.env.DB_PASSWORD"], "vault_wordpress_sites")

    value = result["example.com"]["env"]["DB_HOST"]

    assert template(value, db_host="localhost") == "localhost"


def test_matching_value_in_list_is_left_untemplated():
    result = triage(["vault_wordpress_sites"], "vault_wordpress_sites")

    auth_keys = result["example.com"]["env"]["AUTH_KEYS"]

    assert template(auth_keys[0], first_key="leaked") == "{{ first_key }}"
    assert template(auth_keys[1], second_key="leaked") == "{{ second_key }}"


def test_matching_top_level_scalar_is_left_untemplated():
    result = triage(["vault_users.*.password"], "vault_users")

    value = result["admin"]["password"]

    assert template(value, admin_password="leaked") == "{{ admin_password }}"


def test_non_string_values_pass_through_unchanged():
    result = triage(["vault_wordpress_sites"], "vault_wordpress_sites")

    env = result["example.com"]["env"]

    assert env["DB_PORT"] == 3306
    assert env["DISABLE_WP_CRON"] is True
