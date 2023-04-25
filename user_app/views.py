from allauth.socialaccount.signals import pre_social_login
from django.contrib.auth import get_user_model, login
from django.dispatch.dispatcher import receiver
from djoser.views import TokenCreateView, UserViewSet
from knox.views import LoginView, LogoutAllView, LogoutView
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user_app.serializers.user import (CustomTokenCreateSerializers,
                                       CustomUserCreateAsEmployeeSerializer,
                                       CustomUserCreateCompanyAdminSerializer)

User = get_user_model()


# ----------- user / register user ------------- #
class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == "create":
            data = self.request.data
            if "company" in data:
                company = data["company"]
                if isinstance(company, dict):
                    return CustomUserCreateCompanyAdminSerializer
        return super().get_serializer_class()


# ------------------- login -------------------------- #
class CustomLoginView(LoginView, TokenCreateView):
    serializer_class = CustomTokenCreateSerializers
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(response.data, status=status.HTTP_200_OK)


# --------------------- logout -------------------#
class LogoutView(LogoutView):
    pass


class LogoutAllView(LogoutAllView):
    pass


# ------------- social login --------------- #


@receiver(pre_social_login)
def email_confirmed_(request, sociallogin, **kwargs):
    try:
        user = sociallogin.user
        user.is_active = True
        user.role = "Guest"
        user.save()
    except Exception as e:
        raise serializers.ValidationError({"ERROR": e})
