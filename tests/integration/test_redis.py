from tests.integration.conftest import get, run_cmd


REDIS_SITE_ROOT = "/srv/www/redis.example.com/current"


def test_redis_service_active():
    result = run_cmd("systemctl", "is-active", "redis-server")
    assert result.stdout.strip() == "active"


def test_redis_cli_ping():
    result = run_cmd("redis-cli", "ping")
    assert "PONG" in result.stdout


def test_php_redis_extension():
    result = run_cmd("php", "-m")
    assert "redis" in result.stdout.lower()


def test_redis_basic_read_only_query():
    result = run_cmd("redis-cli", "EXISTS", "__trellis_nonexistent_key__")
    assert result.stdout.strip() in {"0", "1"}


def test_redis_env_vars():
    env_file = f"{REDIS_SITE_ROOT}/.env"

    with open(env_file) as f:
        contents = f.read()

    assert "WP_REDIS_HOST" in contents
    assert "WP_REDIS_PORT" in contents
    assert "WP_REDIS_DATABASE" in contents


def test_redis_site_title(redis_example):
    response = get(redis_example)
    assert response.status_code == 200
    assert "<title>Redis Example" in response.text
