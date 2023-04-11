from django.contrib.auth import authenticate, get_user_model
from djoser.conf import settings
from djoser.serializers import (
    TokenCreateSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


# ------------------- user serializer ------------------ #
# ------------- just for override user data ------------ #
class UserSerializers(UserSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
        )


# ----------------------- register serializer -------------- #
class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "password",
            "name",
            "email",
        )


class CustomTokenCreateSerializers(TokenCreateSerializer):
    default_error_messages = {
        "invalid_credentials": settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR,
        "no_credentials": "email and password are required",
        "not_registered": "Sorry, this is not a registered account.",
        "not_verified": "Please login with your email and verify your account to proceed.",
        "default_case": "something error try again !",
    }

    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not attrs:
            error = "no_credentials"
            raise AuthenticationFailed({"error": [self.error_messages[error]]})

        if not self.user:  # if authenticate failed (line 50)
            self.user = User.objects.filter(**params).first()

            if not self.user:  # if doesn't found the user
                error = "not_registered"
                raise AuthenticationFailed({"error": [self.error_messages[error]]})

            if not self.user.check_password(password):
                error = "invalid_credentials"
                raise AuthenticationFailed({"error": [self.error_messages[error]]})

        if not self.user.is_active:
            error = "not_verified"
            raise AuthenticationFailed({"error": [self.error_messages[error]]})

        if self.user and self.user.is_active:
            attrs["user"] = self.user
            return attrs
        self.fail("default_case")
