from tests.integration.conftest import get


def test_https_site_redirects_from_http():
    response = get("http://example-https.com", allow_redirects=False)

    assert response.status_code in {301, 302}, (
        f"Expected redirect from http://example-https.com, got {response.status_code}. "
        f"Headers: {dict(response.headers)}"
    )
    assert response.headers.get("Location", "").startswith("https://"), (
        f"Expected redirect target to use https scheme, got {response.headers.get('Location')!r}. "
        f"Headers: {dict(response.headers)}"
    )


def test_www_domain_redirects_to_canonical_http():
    response = get("http://www.example.com", allow_redirects=False)

    assert response.status_code in {301, 302}, (
        f"Expected redirect from www domain, got {response.status_code}. "
        f"Headers: {dict(response.headers)}"
    )
    assert response.headers.get("Location", "").startswith("http://example.com"), (
        f"Expected redirect target to canonical host, got {response.headers.get('Location')!r}. "
        f"Headers: {dict(response.headers)}"
    )


def test_https_site_sets_hsts_header(https_example):
    response = get(https_example, verify=False, allow_redirects=False)

    assert "Strict-Transport-Security" in response.headers, (
        "Expected Strict-Transport-Security header on HTTPS site response. "
        f"Headers: {dict(response.headers)}"
    )


def test_nonexistent_page_returns_not_found(http_example):
    response = get(f"{http_example}/definitely-not-a-real-page-for-trellis-tests")

    assert response.status_code == 404, (
        f"Expected 404 for non-existent page, got {response.status_code}. "
        f"Response snippet: {response.text[:240]!r}"
    )
