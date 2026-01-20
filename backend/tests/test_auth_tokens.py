import pytest

@pytest.mark.django_db
def test_obtain_tokens_for_registered_user(api_client, user):
    """
    Should return access+refresh tokens for valid credentials.
    """

    payload = {"username":"testuser", "password":"testpass123"}

    res = api_client.post("/api/token/", payload, format="json")

    assert res.status_code == 200
    assert "access" in res.data
    assert "refresh" in res.data
    assert isinstance(res.data["access"], str) and len(res.data["access"]) > 20
    assert isinstance(res.data["refresh"], str) and len(res.data["refresh"]) > 20

@pytest.mark.django_db
def test_obtain_tokens_for_unregistered_user(api_client, user):
    """
    Should not return access+refresh tokens for invalid credentials.
    """

    payload = {"username":"testuser2", "password":"testpass123"}

    res = api_client.post("/api/token/", payload, format="json")

    assert res.status_code == 401
    assert "access" not in res.data
    assert "refresh" not in res.data

@pytest.mark.django_db
def test_refresh_token(api_client, user):
    """
    Should return a new access token when a valid refresh token is provided.
    """
    payload = {"username":"testuser", "password":"testpass123"}
    res = api_client.post("/api/token/", payload, format="json")

    assert res.status_code == 200
    refresh_token = res.data["refresh"]

    final_res = api_client.post("/api/token/refresh/", {"refresh":refresh_token}, format="json")

    assert final_res.status_code == 200
    assert "access" in final_res.data
    assert isinstance(final_res.data["access"], str)
    assert len(final_res.data["access"]) > 20

@pytest.mark.django_db
def test_invalid_refresh_token(api_client):
    """
    Refresh endpoint should reject invalid refresh tokens.
    """
    res = api_client.post("/api/token/refresh/", {"refresh":"invalid-token"}, format="json")

    assert res.status_code == 401

