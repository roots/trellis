"""Tests for the php_extensions_custom normalization (issue #1666).

The defaults file (roles/php/defaults/main.yml) calls the
`php_extensions` filter on the raw input. The filter is the single
place where list vs. dict coercion happens, so testing the filter
covers both the new list form and the legacy dict form.
"""

from lib.trellis.plugins.filter.filters import php_extensions


def test_filter_expands_list_of_short_names() -> None:
    result = php_extensions(["soap", "gd"], "8.3", "present")
    assert result == {
        "php8.3-soap": "present",
        "php8.3-gd": "present",
    }


def test_filter_passes_legacy_dict_through_unchanged() -> None:
    legacy = {"php8.3-soap": "present"}
    assert php_extensions(legacy, "8.3", "present") is legacy


def test_filter_returns_empty_dict_for_empty_input() -> None:
    assert php_extensions([], "8.3", "present") == {}


def test_filter_returns_empty_dict_for_unexpected_types() -> None:
    assert php_extensions("not-a-list-or-dict", "8.3", "present") == {}
    assert php_extensions(None, "8.3", "present") == {}


def test_filter_uses_provided_php_version() -> None:
    result = php_extensions(["soap"], "8.2", "present")
    assert result == {"php8.2-soap": "present"}


def test_filter_uses_provided_package_state() -> None:
    result = php_extensions(["soap"], "8.3", "latest")
    assert result == {"php8.3-soap": "latest"}
