from tests.integration.conftest import get


def test_non_https_site_title(http_example):
    response = get(http_example)
    assert response.status_code == 200
    assert "<title>Example" in response.text


def test_https_site_title(https_example):
    response = get(https_example, verify=False)
    assert response.status_code == 200
    assert "<title>Example HTTPS" in response.text
