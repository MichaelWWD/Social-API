import pytest
from rest_framework import status
from core import models
from model_bakery import baker
from social.models import Post


@pytest.mark.django_db
class TestCreatePostLike:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        user = models.User.objects.create_user(username='testuser1', password='testpassword2')
        post = baker.make(Post, profile=user.profile)

        response = api_client.post(f'/api/social/posts/{post.id}/likes/', {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_data_is_valid_returns_201(self, api_client, authenticate_profile):
        user = models.User.objects.create_user(username='testuser3', password='testpassword3', email='testuser@mail.com')
        post = baker.make(Post, profile=user.profile)

        authenticate_profile()
        response = api_client.post(f'/api/social/posts/{post.id}/likes/', {})
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrievePostLikes:
    def test_if_post_like_does_not_exist_returns_empty_list(self, api_client, authenticate_profile):
        authenticate_profile
        response = api_client.get(f'/api/social/posts/{0}/likes/')
        assert response.data == []


    def test_if_post_likes_exists_returns_200(self, api_client, authenticate_profile):
        user = models.User.objects.create_user(username='testuser3', password='testpassword3', email='testuser@mail.com')
        post = baker.make(Post, profile=user.profile)

        authenticate_profile()
        api_client.post(f'/api/social/posts/{post.id}/likes/', {})
        response = api_client.get(f'/api/social/posts/{post.id}/likes/')
        assert response.status_code == status.HTTP_200_OK



        