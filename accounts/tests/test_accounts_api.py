import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User,Profile

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def api_client_for_jwt():
    user = User.objects.create_user(email='test@test.com', password='Sduwdsdas&12412')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client

@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="test@test.com", password="Sduwdsdas&12412", is_verified=True,
    )
    return user

@pytest.fixture
def profile(common_user):
    profile = Profile.objects.create(user=common_user,first_name="test firstname",
                                     last_name="test lastname",address="test address",)
    return profile

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

@pytest.fixture
def change_password_data():
    data = {
        "old_password":"Sduwdsdas&12412",
        "new_password":"Aashd123!",
        "new_password1":"Aashd123!",
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
    
    def test_registration_passwords_not_match_400_status(self,api_client):
        """Tests if unauthorized user can't do registration with invalid data(passwords doesn't match)"""
        url = reverse("accounts:api-v1:registration")
        response = api_client.post(url,data={
        "email":"test@test.com",
        "password":"XsKKJEW2121",
        "password1":"ASDADASDWw121",
        })
        assert response.status_code == 400
    
    def test_registration_invalid_password_400_status(self,api_client):
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
        """Tests if unauthorized user can log in with token-login
        also tests the keys that are returned from data(user_id,email,auth_token)"""

        url = reverse("accounts:api-v1:token-login")
        response = api_client.post(url,data=login_data)
        assert response.status_code == 200
        assert len(response.data.keys()) == 3
        assert response.data["email"] == common_user.email
        assert response.data["user_id"] == common_user.id
    
    def test_token_login_invalid_data_status_400(self,api_client,common_user):
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
    
    def test_jwt_create(self,api_client,login_data,common_user):
        url = reverse("accounts:api-v1:jwt-create")
        response = api_client.post(url,data=login_data)

        assert response.status_code == 200
        assert len(response.data.keys()) == 4
        assert response.data["email"] == common_user.email
        assert response.data["user_id"] == common_user.id
    
    def test_jwt_login_api_client(self,login_data,common_user,api_client):
        user = common_user
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse("accounts:api-v1:jwt-create")
        response = api_client.post(url,login_data)

        assert response.status_code == 200
        assert user.is_authenticated == True
    
    def test_authorized_change_password_status_200(self,api_client,common_user,change_password_data):
        url = reverse("accounts:api-v1:change-password")
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.put(url,data=change_password_data)
        assert response.status_code == 200

    def test_change_password_wrong_old_password_status_400(self,api_client,common_user):
        url = reverse("accounts:api-v1:change-password")
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.put(url,data={
        "old_password":"adasdasasd121",
        "new_password":"Aashd123!",
        "new_password1":"Aashd123!",
        })
        assert response.status_code == 400
    
    def test_change_password_new_passwords_not_match_status_400(self,api_client,common_user):
        url = reverse("accounts:api-v1:change-password")
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.put(url,data={
        "old_password":"Sduwdsdas&12412",
        "new_password":"Aashd123!&&",
        "new_password1":"Aashd123!",
        })
        assert response.status_code == 400
    
    def test_unauthorized_change_password_status_401(self,api_client,change_password_data):
        url = reverse("accounts:api-v1:change-password")
        response = api_client.put(url,data=change_password_data)
        assert response.status_code == 401
    
    def test_authorized_get_profile_status_200(self,api_client,common_user):
        url = reverse("accounts:api-v1:profile")
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.get(url)

        assert response.status_code == 200

    def test_authorized_put_profile_status_200(self,api_client,common_user):
        url = reverse("accounts:api-v1:profile")
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.put(url,data={
            "first_name":"test firstname**",
            "last_name":"test lastname**",
            "address":"test address**",
        })

        assert response.status_code == 200
    
    def test_unauthorized_get_profile_status_401(self,api_client):
        url = reverse("accounts:api-v1:profile")
        response = api_client.get(url)

        assert response.status_code == 401
    
    def test_authorized_user_activation_status_200(self,api_client,common_user):
        url = reverse("accounts:api-v1:activation")
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.get(url)

        assert response.status_code == 200
    
    def test_unauthorized_user_activation_status_401(self,api_client):
        url = reverse("accounts:api-v1:activation")
        response = api_client.get(url)

        assert response.status_code == 401
    
    def test_user_activation_confirm_status_200(self,api_client):
        user= User.objects.create_user(
        email="testemail@test.com", password="JKdsdas71&", is_verified=False,
        )
        refresh = RefreshToken.for_user(user)
        url = reverse("accounts:api-v1:activation-confirm",args=[refresh.access_token])
        response = api_client.get(url)

        assert response.status_code == 200
        # assert user.is_verified == True
    
    def test_user_activation_invalid_token_status_400(self,api_client,common_user):
        user=common_user
        refresh = RefreshToken.for_user(user)
        url = reverse("accounts:api-v1:activation-confirm",args=[str(refresh.access_token)+"invalid_token"])
        response = api_client.get(url)

        assert response.status_code == 400

    def test_reset_password_status_200(self,api_client,common_user):
        url = reverse("accounts:api-v1:reset-password")
        response = api_client.post(url,data={"email":"test@test.com"})

        assert response.status_code == 200
    
    def test_reset_password_invalid_email_status_400(self,api_client,common_user):
        url = reverse("accounts:api-v1:reset-password")
        response = api_client.post(url,data={"email":"notfounduser@email.com"})

        assert response.status_code == 400
