import pytest
from rest_framework import status
from core import models
from model_bakery import baker
from social.models import Post


@pytest.fixture
def create_post(api_client):
    def do_create_post(post):
        return api_client.post('/api/social/posts/', post)
    return do_create_post


@pytest.mark.django_db
class TestCreatePost:
    def test_if_user_is_anonymous_returns_401(self, create_post):
        response = create_post({'content': 'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_returns_400(self, api_client, authenticate_profile, create_post):
        authenticate_profile()
        response = create_post({'uploaded_files': 'a' })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, api_client, authenticate_profile, create_post):
        authenticate_profile()
        response = create_post({'content': 'a'})
        assert response.status_code == status.HTTP_201_CREATED




@pytest.mark.django_db
class TestRetrievePost:
    def test_if_post_does_not_exist_returns_404(self, api_client):
        response = api_client.get(f'/api/social/posts/{0}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


    def test_if_post_exists_returns_200(self, api_client):
        user = models.User.objects.create_user(username='testuser1', password='testpassword2')
        post = baker.make(Post, profile=user.profile)
        response = api_client.get(f'/api/social/posts/{post.id}/')
        assert response.status_code == status.HTTP_200_OK



        