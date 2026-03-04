"""Render Trellis Jinja templates with Ansible's Templar.

Contract:
- Inputs: a template path relative to repository root and optional variable overrides.
- Baseline context: role defaults plus the baseline scenario fixture.
- Merge behavior: recursive dict merge where override values replace baseline leaves.
"""

from __future__ import annotations

import os
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCENARIOS_DIR = Path(__file__).resolve().parent / "scenarios"
ANSIBLE_TMP_DIR = REPO_ROOT / ".ansible" / "tmp"

# Keep Ansible state under the repository so tests run in restricted sandboxes.
ANSIBLE_TMP_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("ANSIBLE_LOCAL_TEMP", str(ANSIBLE_TMP_DIR))
os.environ.setdefault("ANSIBLE_HOME", str(REPO_ROOT / ".ansible"))

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

try:
    # ansible-core >= 2.18
    from ansible.template import trust_as_template
except ImportError:  # pragma: no cover - compatibility for older Ansible versions
    def trust_as_template(value: str) -> str:
        return value

DEFAULTS_FILES = (
    REPO_ROOT / "roles/nginx/defaults/main.yml",
    REPO_ROOT / "roles/wordpress-setup/defaults/main.yml",
)


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        content = yaml.safe_load(handle) or {}
    if not isinstance(content, dict):
        raise TypeError(f"Expected mapping in {path}, got {type(content).__name__}")
    return content


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def _derive_template_vars(variables: dict[str, Any]) -> dict[str, Any]:
    vars_copy = deepcopy(variables)
    item = vars_copy.get("item", {})
    item_value = item.get("value", {}) if isinstance(item, dict) else {}

    cache_config = item_value.get("cache", {}) if isinstance(item_value, dict) else {}
    ssl_config = item_value.get("ssl", {}) if isinstance(item_value, dict) else {}
    multisite_config = item_value.get("multisite", {}) if isinstance(item_value, dict) else {}

    if "fastcgi_cache_enabled" not in vars_copy:
        vars_copy["fastcgi_cache_enabled"] = bool(cache_config.get("enabled", False))
    if "ssl_enabled" not in vars_copy:
        vars_copy["ssl_enabled"] = bool(ssl_config.get("enabled", False))

    if "site_hosts_canonical" not in vars_copy:
        hosts = item_value.get("site_hosts", []) if isinstance(item_value, dict) else []
        vars_copy["site_hosts_canonical"] = [h.get("canonical") for h in hosts if h.get("canonical")]

    vars_copy.setdefault("site_hosts_redirects", [])
    vars_copy.setdefault("multisite_subdomains_wildcards", [])

    # Keep this explicit to avoid accidental truthy behavior from templated defaults.
    vars_copy.setdefault("robots_tag_header_enabled", False)
    vars_copy.setdefault("h5bp_cache_file_descriptors_enabled", True)
    vars_copy.setdefault("h5bp_extra_security_enabled", True)
    vars_copy.setdefault("h5bp_no_transform_enabled", False)
    vars_copy.setdefault("h5bp_x_ua_compatible_enabled", True)
    vars_copy.setdefault("h5bp_cache_busting_enabled", False)
    vars_copy.setdefault("h5bp_cross_domain_fonts_enabled", True)
    vars_copy.setdefault("h5bp_expires_enabled", False)
    vars_copy.setdefault("h5bp_protect_system_files_enabled", True)

    # Ensure multisite flags always exist for tests that toggle rewrites.
    if isinstance(multisite_config, dict):
        multisite_config.setdefault("enabled", False)
        multisite_config.setdefault("subdomains", False)
        item_value["multisite"] = multisite_config
        item["value"] = item_value
        vars_copy["item"] = item

    return vars_copy


def build_vars(overrides: dict[str, Any] | None = None, scenario: str = "baseline") -> dict[str, Any]:
    variables: dict[str, Any] = {}

    for defaults_file in DEFAULTS_FILES:
        variables = _deep_merge(variables, _load_yaml(defaults_file))

    scenario_vars = _load_yaml(SCENARIOS_DIR / f"{scenario}.yml")
    variables = _deep_merge(variables, scenario_vars)

    if overrides:
        variables = _deep_merge(variables, overrides)

    return _derive_template_vars(variables)


def render_template(template_path: str, overrides: dict[str, Any] | None = None, scenario: str = "baseline") -> str:
    template = REPO_ROOT / template_path
    data_loader = DataLoader()
    data_loader.set_basedir(str(REPO_ROOT))

    templar = Templar(loader=data_loader, variables=build_vars(overrides=overrides, scenario=scenario))
    contents = template.read_text(encoding="utf-8")
    return templar.template(
        trust_as_template(contents),
        preserve_trailing_newlines=True,
        fail_on_undefined=True,
        escape_backslashes=False,
    )
