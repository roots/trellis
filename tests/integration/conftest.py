"""Integration test fixtures and helpers.

Tests assume provision/deploy/install have already completed in prior
workflow steps. All tests are read-only — no destructive mutations to
the running environment.
"""

from __future__ import annotations

import subprocess

import pytest
import requests


# Site base URLs matching the integration workflow's /etc/hosts and deploy steps.
SITES = {
    "example.com": "http://example.com",
    "example-https.com": "https://example-https.com",
    "redis.example.com": "http://redis.example.com",
}


@pytest.fixture()
def http_example():
    return SITES["example.com"]


@pytest.fixture()
def https_example():
    return SITES["example-https.com"]


@pytest.fixture()
def redis_example():
    return SITES["redis.example.com"]


def get(url: str, **kwargs) -> requests.Response:
    """GET helper with explicit timeout and caller-controlled TLS verification."""
    kwargs.setdefault("timeout", 10)
    return requests.get(url, **kwargs)


def head(url: str, **kwargs) -> requests.Response:
    """HEAD helper with explicit timeout and caller-controlled TLS verification."""
    kwargs.setdefault("timeout", 10)
    return requests.head(url, **kwargs)


def run_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return the result. Raises on non-zero exit."""
    return subprocess.run(args, capture_output=True, text=True, check=True)
