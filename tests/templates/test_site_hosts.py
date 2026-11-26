"""Host lists must keep their configured order.

Ansible's `union` filter returns set order (ansible-core >= 2.16), which
changes between runs because Python randomizes string hashes per process.
Host lists feed config files and the Let's Encrypt certificate ID, so an
unstable order makes provisioning report changes (and can request new
certificates) when nothing changed. The lists below are long enough that a
set returning them in configured order by chance is very unlikely.
"""

from __future__ import annotations

from tests.templates.render import render_helper, render_template

SITE = {
    "key": "example.com",
    "value": {
        "site_hosts": [
            {"canonical": "example.com", "redirects": ["www.example.com", "old.example.com"]},
            {"canonical": "example.org", "redirects": ["www.example.org"]},
            {"canonical": "example.net"},
            {"canonical": "example.dev", "redirects": ["www.example.dev"]},
        ],
    },
}

CANONICAL = ["example.com", "example.org", "example.net", "example.dev"]
ALL_HOSTS = CANONICAL + ["www.example.com", "old.example.com", "www.example.org", "www.example.dev"]
WILDCARDS = ["*.example.com", "*.example.org", "*.example.net", "*.example.dev"]


def test_site_hosts_keeps_canonical_then_redirects_order() -> None:
    assert render_helper("site_hosts", {"item": SITE}) == ALL_HOSTS


def test_site_hosts_keeps_first_occurrence_of_duplicates() -> None:
    site = {
        "key": "example.com",
        "value": {
            "site_hosts": [
                {"canonical": "example.com", "redirects": ["www.example.com", "example.org"]},
                {"canonical": "example.org", "redirects": ["www.example.com"]},
            ],
        },
    }

    assert render_helper("site_hosts", {"item": site}) == ["example.com", "example.org", "www.example.com"]


def test_wordpress_site_server_name_keeps_order() -> None:
    rendered = render_template(
        "roles/wordpress-setup/templates/wordpress-site.conf.j2",
        overrides={"site_hosts_canonical": CANONICAL, "multisite_subdomains_wildcards": WILDCARDS},
    )

    assert f"server_name {' '.join(CANONICAL + WILDCARDS)};" in rendered


def test_self_signed_openssl_config_keeps_order() -> None:
    rendered = render_template(
        "roles/wordpress-setup/templates/self-signed-openssl-config.j2",
        overrides={
            "item": SITE,
            "site_hosts": ALL_HOSTS,
            "multisite_subdomains_wildcards": WILDCARDS,
        },
    )

    sans = ",".join(f"DNS:{host}" for host in ALL_HOSTS + WILDCARDS)
    assert f"subjectAltName = {sans}\n" in rendered
    assert "commonName = example.com\n" in rendered
