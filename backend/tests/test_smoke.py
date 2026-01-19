import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_experiments_list_requires_auth():
    """
    Smoke test: endpoint should reject unauthenticated requests.
    """
    client = APIClient()
    res = client.get("/api/experiments/")
    assert res.status_code in (401, 403)
