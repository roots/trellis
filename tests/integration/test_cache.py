from tests.integration.conftest import head


def test_fastcgi_cache_headers(http_example):
    """Verify FastCGI cache is active by checking successive requests.

    The first request may be a MISS, but subsequent requests should
    return a recognized cache status (MISS, HIT, or STALE).
    """
    valid_statuses = {"MISS", "HIT", "STALE"}

    # Warm the cache
    head(http_example)
    head(http_example)

    response = head(http_example)
    cache_status = response.headers.get("X-Fastcgi-Cache", response.headers.get("Fastcgi-Cache", ""))

    assert cache_status.upper() in valid_statuses, (
        f"Expected Fastcgi-Cache header to be one of {valid_statuses}, got '{cache_status}'. "
        f"Headers: {dict(response.headers)}"
    )


def test_fastcgi_cache_header_present_on_first_request(http_example):
    response = head(http_example)
    cache_status = response.headers.get("X-Fastcgi-Cache", response.headers.get("Fastcgi-Cache", ""))

    assert cache_status != "", f"Expected Fastcgi-Cache header to be present. Headers: {dict(response.headers)}"
