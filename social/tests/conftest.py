import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from core import models



@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=True):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate

@pytest.fixture
def authenticate_profile(api_client):
    def do_authenticate_profile(username='testuser', password='testpassword'):
        user = models.User.objects.create_user(username=username, password=password)
        return api_client.force_authenticate(user=user)
    return do_authenticate_profile

