from django.contrib.auth import authenticate, get_user_model
from djoser.conf import settings
from djoser.serializers import (
    TokenCreateSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from public_apps.company.models import Company
from public_apps.employee.models import Employee
from user_app.serializers.company_relations import UserEmployeeSerializer
from hashid_field import HashidField
from hashid_field.rest import HashidSerializerCharField


User = get_user_model()


# ------------------- user serializer ------------------ #
# ------------- just for override user data ------------ #
class UserSerializers(UserSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
        )


# ----------------------- register serializer -------------- #


class CustomUserCreateSerializer(UserCreateSerializer):
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        many=False,
        required=True,
    )
    employee = UserEmployeeSerializer(many=False, required=True)

    class Meta:
        model = User
        fields = ("id", "password", "username", "email", "role", "company", "employee")
        extra_kwargs = {
            "role": {"read_only": False, "required": True},
        }

    def validate(self, attrs):
        password = attrs.get("password")
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        company_data = validated_data.pop("company")
        employee_data = validated_data.pop("employee")

        # --------------------- company creation ---------------- #
        if isinstance(company_data, dict):
            create_company = True
            company = Company.objects.create(**company_data)
        else:
            create_company = False
            company = company_data

        user = super().create(validated_data)

        # ---------------------- employee creation ------------------- #
        try:
            Employee.objects.create(user=user, company=company, **employee_data)
        except Exception as e:
            raise serializers.ValidationError({"error": e})

        # ----------- company fields --------- #
        if create_company:
            company.owner = user
            company.save()
        else:
            user.company = company
        return user


# ------------------- login --------------------- #
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
