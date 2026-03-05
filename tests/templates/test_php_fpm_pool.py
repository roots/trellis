from tests.templates.render import render_template


def test_render_php_fpm_pool_default_runtime_user() -> None:
    rendered = render_template(
        "roles/wordpress-setup/templates/php-fpm-pool-wordpress.conf.j2",
        overrides={"web_user": "web", "web_group": "www-data"},
    )

    assert "user = web" in rendered
    assert "group = www-data" in rendered
    assert "php_admin_value[open_basedir] = /srv/www/:/tmp" in rendered


def test_render_php_fpm_pool_hardened_runtime_user() -> None:
    rendered = render_template(
        "roles/wordpress-setup/templates/php-fpm-pool-wordpress.conf.j2",
        overrides={
            "web_user": "web",
            "web_group": "www-data",
            "wordpress_runtime_hardened": True,
            "wordpress_runtime_user": "php-runner",
            "wordpress_runtime_group": "php-runner",
        },
    )

    assert "user = php-runner" in rendered
    assert "group = php-runner" in rendered
