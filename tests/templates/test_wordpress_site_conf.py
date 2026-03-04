import pytest

from tests.templates.render import render_template


@pytest.mark.xfail(strict=True, reason="#1594")
def test_cache_directives_scope_to_200_and_skip_location_responses() -> None:
    rendered = render_template("roles/wordpress-setup/templates/wordpress-site.conf.j2")

    assert "fastcgi_cache_valid 200 30s;" in rendered
    assert "fastcgi_no_cache $skip_cache $upstream_http_location;" in rendered


def test_cache_directives_absent_when_cache_disabled() -> None:
    rendered = render_template(
        "roles/wordpress-setup/templates/wordpress-site.conf.j2",
        overrides={
            "fastcgi_cache_enabled": False,
            "item": {"value": {"cache": {"enabled": False}}},
        },
    )

    assert "fastcgi_cache wordpress;" not in rendered
    assert "fastcgi_cache_valid" not in rendered
    assert "fastcgi_no_cache" not in rendered


@pytest.mark.xfail(strict=True, reason="#1548")
def test_multisite_subdirectory_rewrite_uses_request_uri() -> None:
    rendered = render_template(
        "roles/wordpress-setup/templates/wordpress-site.conf.j2",
        overrides={
            "item": {
                "value": {
                    "multisite": {
                        "enabled": True,
                        "subdomains": False,
                    }
                }
            }
        },
    )

    assert "rewrite /wp-admin$ $scheme://$host$request_uri/ permanent;" in rendered
    assert "rewrite /wp-admin$ $scheme://$host$uri/ permanent;" not in rendered


def test_multisite_subdomain_rewrites_present() -> None:
    rendered = render_template(
        "roles/wordpress-setup/templates/wordpress-site.conf.j2",
        overrides={
            "item": {
                "value": {
                    "multisite": {
                        "enabled": True,
                        "subdomains": True,
                    }
                }
            }
        },
    )

    assert "rewrite ^/(wp-.*.php)$ /wp/$1 last;" in rendered
    assert "rewrite ^/(wp-(content|admin|includes).*) /wp/$1 last;" in rendered
