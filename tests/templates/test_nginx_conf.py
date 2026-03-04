import pytest

from tests.templates.render import render_template


@pytest.mark.xfail(strict=True, reason="#1551")
def test_cache_use_stale_excludes_updating_by_default() -> None:
    rendered = render_template("roles/nginx/templates/nginx.conf.j2")

    assert "fastcgi_cache_use_stale error timeout invalid_header http_500;" in rendered
    assert "fastcgi_cache_use_stale updating error timeout invalid_header http_500;" not in rendered


def test_cache_use_stale_includes_updating_when_enabled() -> None:
    # On current master this passes because `updating` is hardcoded, not because
    # `nginx_cache_use_stale_updating` is wired yet. It becomes the real toggle
    # assertion once #1551 lands.
    rendered = render_template(
        "roles/nginx/templates/nginx.conf.j2",
        overrides={"nginx_cache_use_stale_updating": True},
    )

    assert "fastcgi_cache_use_stale updating error timeout invalid_header http_500;" in rendered
