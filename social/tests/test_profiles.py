import pytest
from django.contrib.auth.models import User
from rest_framework import status


@pytest.mark.django_db
class TestRetrieveCurrentProfile:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get(f'/api/social/profiles/details/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_profile_exists_returns_200(self, api_client, authenticate_profile):
        authenticate_profile()
        response = api_client.get(f'/api/social/profiles/details/')
        assert response.status_code == status.HTTP_200_OK



@pytest.mark.django_db
class TestUpdateCurrentProfile:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.put(f'/api/social/profiles/details/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_profile_exists_returns_200(self, api_client, authenticate_profile):
        authenticate_profile()
        response = api_client.put(f'/api/social/profiles/details/', {"bio": "string"})
        assert response.status_code == status.HTTP_200_OK