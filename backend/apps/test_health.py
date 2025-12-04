"""Tests for health check endpoints"""

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.integration
class TestHealthChecks:
    """Test health check endpoints"""

    def test_healthz_endpoint(self, api_client):
        """Test basic health check"""
        url = reverse("healthz")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "healthy"

    def test_livez_endpoint(self, api_client):
        """Test liveness probe"""
        url = reverse("livez")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "alive"

    def test_readyz_endpoint(self, api_client):
        """Test readiness probe"""
        url = reverse("readyz")
        response = api_client.get(url)
        # May fail if Redis is not running, but should return proper structure
        assert "status" in response.json()
        assert "checks" in response.json()
        assert "database" in response.json()["checks"]
        assert "cache" in response.json()["checks"]
