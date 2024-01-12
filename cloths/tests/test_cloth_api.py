import pytest
from rest_framework.test import APIClient
from django.urls import reverse

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
def super_user():
    user = User.objects.create_superuser(
        email="admin@admin.com", password="Sduwdsdas&1241289",
    )
    return user

@pytest.fixture
def data():
    data = {"title": "test", "description": "test description",
        "price":150000,"active":True,"season":"winter","gender":"male",}
    return data

@pytest.mark.django_db
class TestClothApi():
    def test_get_cloth_unauthorized_response_200_status(self, api_client):
        "Tests if unauthorized user's get request to cloth-list is successful"
        url = reverse("cloths:api-v1:cloth-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_post_cloth_unauthorized_response_401_status(self, api_client,data):
        "Tests if unauthorized users can't create new cloth or post request is not successful"
        url = reverse("cloths:api-v1:cloth-list")
        response = api_client.post(url,data)
        assert response.status_code == 401
    
    def test_post_cloth_common_user_response_403_status(self, api_client,common_user,data):
        "Tests if common users can't create new cloth or post request is not successful"
        url = reverse("cloths:api-v1:cloth-list")
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url,data)
        assert response.status_code == 403

    def test_post_cloth_super_user_response_201_status(self, api_client,super_user,data):
        "Tests if superusers can create new cloth or post request is successful"
        url = reverse("cloths:api-v1:cloth-list")
        user = super_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url,data)
        assert response.status_code == 201
    
    def test_post_cloth_invalid_data_response_400_status(self, api_client,super_user):
        "Tests if superusers can't create new cloth with invalid data"
        url = reverse("cloths:api-v1:cloth-list")
        user = super_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url,data={"title":"test invalid data","description":"test invalid description"})
        assert response.status_code == 400
        
    def test_post_cloth_super_user_data(self, api_client,super_user,data):
        "Tests the content of the created cloth"
        url = reverse("cloths:api-v1:cloth-list")
        user = super_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url,data)

        assert response.data["title"] == "test"
        assert response.data["description"] == "test description"
        assert response.data["price"] == 150000
