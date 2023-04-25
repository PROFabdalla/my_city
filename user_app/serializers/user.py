from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from djoser.conf import settings
from djoser.serializers import (TokenCreateSerializer, UserCreateSerializer,
                                UserSerializer)
from hashid_field import HashidField
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from core.utils.base import CustomModelSerializer
from public_apps.company.models import Company
from public_apps.employee.models import Employee
from user_app.models import User
from user_app.serializers.company_relations import (
    UserCompanySerializer, UserEmployeeAdminSerializer, UserEmployeeSerializer)


# ------------------- user serializer ------------------ #
# ------------- just for override user data ------------ #
class UserSerializers(UserSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_admin", "is_company_admin", "role")


# /////////////////////////////////////////////////////////////
# ----------------------- register serializer -------------- #
# /////////////////////////////////////////////////////////////
# ------------------ if user in existing company ------------------- #
class CustomUserCreateAsEmployeeSerializer(CustomModelSerializer, UserCreateSerializer):
    company = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        queryset=Company.objects.all(),
        many=False,
        required=False,
    )
    employee = UserEmployeeSerializer(many=False, required=False)

    class Meta:
        model = User
        fields = ("id", "password", "username", "email", "role", "company", "employee")
        extra_kwargs = {
            "role": {"read_only": True, "required": False},
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
        role = "citizen"
        if "company" and "employee" in validated_data:
            role = "employee"
            employee_data = validated_data.pop("employee")
            company_data = validated_data.pop("company")

        user = super().create(validated_data)

        # --------------------- company creation ---------------- #
        if role == "employee":
            user.role = "employee"
            user.is_company_admin = False
            user.save()
            company = company_data
            Employee.objects.create(user=user, company=company, **employee_data)
        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.role == "employee":
            rep["company"] = UserCompanySerializer(instance.employee.company).data
        return rep


# ----------- if user is company admin -------------#
class CustomUserCreateCompanyAdminSerializer(
    CustomModelSerializer, UserCreateSerializer
):
    employee = UserEmployeeAdminSerializer(many=False, required=False)
    company = UserCompanySerializer(required=False, many=False)

    class Meta:
        model = User
        fields = ("id", "password", "username", "email", "role", "company", "employee")
        extra_kwargs = {
            "role": {"read_only": True, "required": False},
        }

    def validate(self, attrs):
        print(self.context["request"].data)
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
        employee_data = validated_data.pop("employee")
        company_data = validated_data.pop("company")
        if isinstance(company_data, dict):
            user = super().create(validated_data)
            company = Company.objects.create(owner=user, **company_data)
            user.is_company_admin = True
            user.role = "employee"
            user.save()
            Employee.objects.create(user=user, company=company, **employee_data)
            return user


# ------------------- login --------------------- #
class CustomTokenCreateSerializers(TokenCreateSerializer):
    default_error_messages = {
        "invalid_credentials": settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR,
        "no_credentials": "email and password are required",
        "not_registered": "Sorry, this is not a registered account.",
        "not_verified": "Please login with your email and verify your account to proceed.",
        "company_not_verified": "Please verify your company to proceed, contact site admin .",
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

        if self.user.role == "employee":
            if self.user.employee.company.active == False:
                error = "company_not_verified"
                raise AuthenticationFailed({"error": [self.error_messages[error]]})

        if self.user and self.user.is_active:
            attrs["user"] = self.user
            return attrs
        self.fail("default_case")
