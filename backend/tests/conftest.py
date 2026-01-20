import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    # Create a default user for authentication tests
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="testpass123")