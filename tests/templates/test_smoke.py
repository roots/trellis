from tests.templates.render import render_template


def test_render_wordpress_site_template_smoke() -> None:
    rendered = render_template("roles/wordpress-setup/templates/wordpress-site.conf.j2")

    assert "# test-managed" in rendered
    assert "server {" in rendered
    assert "fastcgi_pass unix:/var/run/php-fpm-wordpress.sock;" in rendered
