from tests.templates.render import render_template


def test_cache_use_stale_excludes_updating_by_default() -> None:
    rendered = render_template("roles/nginx/templates/nginx.conf.j2")

    assert "fastcgi_cache_use_stale error timeout invalid_header http_500;" in rendered
    assert "fastcgi_cache_use_stale updating error timeout invalid_header http_500;" not in rendered


def test_cache_use_stale_includes_updating_when_enabled() -> None:
    rendered = render_template(
        "roles/nginx/templates/nginx.conf.j2",
        overrides={"nginx_cache_use_stale": "updating error timeout invalid_header http_500"},
    )

    assert "fastcgi_cache_use_stale updating error timeout invalid_header http_500;" in rendered
