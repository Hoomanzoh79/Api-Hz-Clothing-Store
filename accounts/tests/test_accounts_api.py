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
def data():
    data = {
        "email":"test@test.com",
        "password":"XsKKJEW2121",
        "password1":"XsKKJEW2121",
    }
    return data

@pytest.mark.django_db
class TestAccountApi():
    def test_registration_api_view_201_status(self,api_client,data):
        url = reverse("accounts:api-v1:registration")
        response = api_client.post(url,data=data)
        assert response.status_code == 201