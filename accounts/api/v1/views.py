from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveUpdateAPIView
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer,
)
from accounts.permissions import IsNotAuthenticated
from accounts.models import User, Profile


class RegistrationApiView(GenericAPIView):
    """For registering new users"""

    serializer_class = RegistrationSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_email = serializer.validated_data["email"]
            data = {
                "email": user_email,
            }
            user_obj = get_object_or_404(User, email=user_email)
            token = self.get_tokens_for_user(user_obj)
            message = EmailMessage(
                "email/activation.tpl",
                {"token": token},
                "admin@admin.com",
                to=[user_email],
            )
            message.send()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomAuthToken(ObtainAuthToken):
    """For token login"""
    permission_classes = [IsNotAuthenticated]
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
            }
        )


class DiscardAuthToken(APIView):
    """For token logout"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    """For jwt login"""

    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(GenericAPIView):
    """
    An endpoint for changing password
    """

    serializer_class = ChangePasswordSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password changed successfully"},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """getting user without pk or lookup field"""
        queryset = self.get_queryset()
        # getting the user that's logged in
        logged_in_user = get_object_or_404(queryset, user=self.request.user)
        return logged_in_user


class TestEmailSend(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # you can use threading to send emails faster
        user = request.user
        message = EmailMessage(
            "email/hello.tpl", {"user": user}, "admin@gmail.com", to=[user.email]
        )
        message.send()
        return Response("email sent!")


class UserActivationApiView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # you can use threading to send emails faster
        user = request.user
        if not user.is_verified:
            token = self.get_tokens_for_user(user)
            message = EmailMessage(
                "email/activation.tpl",
                {"user": user, "token": token},
                "admin@gmail.com",
                to=[user.email],
            )
            message.send()
            return Response("email sent!")
        return Response("user already verified")

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class UserActivationConfirmApiView(GenericAPIView):
    def get(self, request, token, *args, **kwargs):
        # decode token
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            # find user id
            user_id = token.get("user_id")
        # exception handlings
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "token is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # find user from id
        user = get_object_or_404(User, pk=user_id)
        # for users that are already verified
        if user.is_verified:
            return Response({"details": "your account has already been verified"})
        # activate user
        user.is_verified = True
        user.save()
        return Response({"details": "your account has been verified"})


class ResetPasswordApiView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        # you can use threading to send emails faster
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data["email"]
            user = get_object_or_404(User, email=user_email)
            token = self.get_tokens_for_user(user)
            message = EmailMessage(
                "email/reset_password.tpl",
                {"user": user, "token": token},
                "admin@gmail.com",
                to=[user_email],
            )
            message.send()
            return Response("reset password email has been sent")
        return Response(serializer.errors)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ResetPasswordConfirmApiView(GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, token, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # decode token
            try:
                token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                # find user id
                user_id = token.get("user_id")
            # exception handlings
            except ExpiredSignatureError:
                return Response(
                    {"details": "token has been expired"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except InvalidSignatureError:
                return Response(
                    {"details": "token is invalid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # find user from id
            user = get_object_or_404(User, pk=user_id)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(
                {"details": "password has been reset successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
