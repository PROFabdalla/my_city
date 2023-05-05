from allauth.socialaccount.signals import pre_social_login, social_account_added
from django.contrib.auth import login
from django.dispatch.dispatcher import receiver
from djoser.views import TokenCreateView, UserViewSet
from knox.views import LoginView, LogoutAllView, LogoutView
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user_app.serializers.user import (
    CustomTokenCreateSerializers,
    CustomUserCreateAsEmployeeSerializer,
    CustomUserCreateCompanyAdminSerializer,
    SocialUserSerializers,
)
from rest_framework import generics
from user_app.models import User
from rest_framework.permissions import IsAuthenticated

from knox.models import AuthToken


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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            fields=["username", "email", "password"],
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


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
def email_confirmed(request, sociallogin, **kwargs):
    user = sociallogin.user
    if user.is_active == False:
        user.is_active = True
        user.role = "citizen"


class SocialLoginToken(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SocialUserSerializers
    permission_classes = [AllowAny]

    def get_queryset(self):
        data = self.request.data
        user = data["email"]
        queryset = User.objects.filter(email=user)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        data = self.request.data
        email = data["email"]
        user = User.objects.filter(email=email).first()
        token = AuthToken.objects.create(user=user)
        if token:
            context["token"] = token[1]
        return context
