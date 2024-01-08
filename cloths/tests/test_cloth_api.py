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
        email="admin@admin.com", password="Sduwdsdas&12412", is_verified=True,
    )
    return user

@pytest.mark.django_db
class TestClothApi():
    def test_get_cloth_response_200_status(self, api_client):
        url = reverse("cloths:api-v1:cloth-list")
        response = api_client.get(url)
        assert response.status_code == 200
