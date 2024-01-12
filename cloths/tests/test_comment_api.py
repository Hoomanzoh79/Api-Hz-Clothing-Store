import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from cloths.models import Cloth,Comment

from accounts.models import User

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="test@test.com", password="Sduwdsdas&12412", is_verified=True,
    )
    return user

@pytest.fixture
def cloth_example():
    cloth = Cloth.objects.create(title="test",description="test description",
            price=150000,active=True,season="winter",gender="male",)

    return cloth

@pytest.fixture
def comment_example(cloth_example):
    comment = Comment.objects.create(body="test comment",active=True,cloth=cloth_example)
    return comment

@pytest.fixture
def data():
    data = {"body":"test comment","active":True}
    return data

@pytest.mark.django_db
class TestCommentApi():
    def test_get_comment_list_unauthorized_response_200_status(self, api_client,cloth_example):
        "Tests if unauthorized user's get request to comment list is successful"
        url = reverse("cloths:api-v1:comment_list",args=[cloth_example.id])
        response = api_client.get(url)
        assert response.status_code == 200
    
    def test_post_comment_list_unauthorized_response_401_status(self, api_client,cloth_example,data):
        "Tests if unauthorized users can't create new comment or post request is not successful"
        url = reverse("cloths:api-v1:comment_list",args=[cloth_example.id])
        response = api_client.post(url,data=data)
        assert response.status_code == 401
        
    def test_post_comment_list_authorized_response_201_status(self, api_client,common_user,cloth_example,data):
        "Tests if authorized users can create new comment or post request is successful"
        url = reverse("cloths:api-v1:comment_list",args=[cloth_example.id])
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url,data=data)
        assert response.status_code == 201
    
    def test_get_comment_detail_response_200_status(self, api_client,cloth_example,comment_example):
        "Tests if all the user's get requests to comment detail is successful"
        url = reverse("cloths:api-v1:comment_detail",args=[cloth_example.id,comment_example.id])
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["body"] == "test comment"
        assert response.data["cloth"] == cloth_example.title

    def test_get_comment_detail_invalid_id_response_400_status(self, api_client,comment_example):
        "Tests if all the user's get requests to comment detail is not successful with invalid cloth id"
        url = reverse("cloths:api-v1:comment_detail",args=[3123132,comment_example.id])
        response = api_client.get(url)
        assert response.status_code == 400