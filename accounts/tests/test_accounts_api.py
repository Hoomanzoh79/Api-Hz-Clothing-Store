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
def registration_data():
    data = {
        "email":"test@gmail.com",
        "password":"XsKKJEW2121",
        "password1":"XsKKJEW2121",
    }
    return data

@pytest.fixture
def login_data():
    data = {
        "email":"test@test.com",
        "password":"Sduwdsdas&12412",
    }
    return data
@pytest.mark.django_db
class TestAccountApi():
    def test_unauthorized_registration_201_status(self,api_client,registration_data):
        """Tests if unauthorized user can do registration with valid data"""
        url = reverse("accounts:api-v1:registration")
        response = api_client.post(url,data=registration_data)
        assert response.status_code == 201
        assert response.data["email"] == registration_data["email"]
    
    def test_unauthorized_registration_password_not_match_400_status(self,api_client):
        """Tests if unauthorized user can't do registration with invalid data(passwords doesn't match)"""
        url = reverse("accounts:api-v1:registration")
        response = api_client.post(url,data={
        "email":"test@test.com",
        "password":"XsKKJEW2121",
        "password1":"ASDADASDWw121",
        })
        assert response.status_code == 400
    
    def test_unauthorized_registration_invalid_password_400_status(self,api_client):
        """checks if unauthorized user can't do registration with 
        invalid data(password too common,too short and entirely numeric)"""
        url = reverse("accounts:api-v1:registration")
        response = api_client.post(url,data={
        "email":"test@test.com",
        "password":"1234",
        "password1":"1234",
        })
        assert response.status_code == 400
    
    def test_authorized_registration_403_status(self,api_client,registration_data,common_user):
        """Tests if authorized user can't do registration"""
        url = reverse("accounts:api-v1:registration")
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url,data=registration_data)
        assert response.status_code == 403
    
    def test_unauthorized_token_login_status_200(self,api_client,login_data,common_user):
        """Tests if unauthorized user can log in with token-login"""
        url = reverse("accounts:api-v1:token-login")
        response = api_client.post(url,data=login_data)
        assert response.status_code == 200
        assert response.data["email"] == login_data["email"]
        assert response.data["user_id"] == common_user.id
    
    def test_unauthorized_token_login_invalid_data_status_400(self,api_client,common_user):
        """Tests if unauthorized user can't log in with invalid data"""
        url = reverse("accounts:api-v1:token-login")
        response = api_client.post(url,data={
        "email":"invalid_email@gmail.com",
        "password":"Sduwdsdas&12412",
        })
        assert response.status_code == 400
    
    def test_authorized_token_login_status_403(self,api_client,login_data,common_user):
        """Tests if authorized user can't log in with token-login"""
        url = reverse("accounts:api-v1:token-login")
        user= common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url,data=login_data)
        assert response.status_code == 403
    
    def test_authorized_token_logout_status_204(self,api_client,common_user,login_data):
        """Tests if authorized user can log out with token-logout and if their auth_token is deleted"""
        url = reverse("accounts:api-v1:token-login")
        api_client.post(url,data=login_data)
        user = common_user
        api_client.force_authenticate(user=user)
        url = reverse("accounts:api-v1:token-logout")
        response = api_client.post(url)
        assert response.status_code == 204
        assert user.auth_token != True
    
    def test_unauthorized_token_logout_status_401(self,api_client):
        """Tests if unauthorized user can't log out with token-logout"""
        url = reverse("accounts:api-v1:token-logout")
        response = api_client.post(url)
        assert response.status_code == 401