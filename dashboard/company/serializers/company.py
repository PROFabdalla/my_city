from hashid_field import HashidField
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from core.utils.base import CustomModelSerializer
from dashboard.company.serializers.company_relations import (
    DHB_CompanyAddressesSerializer,
    DHB_CompanyEmployeesSerializer,
    DHB_CompanyOwnerSerializer,
)
from public_apps.company.models import Company
from public_apps.addresses.models import Addresses


class DHB_CompanySerializer(CustomModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        many=False,
        required=False,
        read_only=True,
    )
    employees = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        many=True,
        required=False,
        read_only=True,
    )
    addresses = serializers.PrimaryKeyRelatedField(
        queryset=Addresses.objects.all(),
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        many=True,
        required=False,
    )

    class Meta:
        model = Company
        fields = (
            "id",
            "title",
            "owner",
            "business_description",
            "phone_number",
            "role",
            "employees",
            "addresses",
        )

        expandable_fields = {
            "owner": (DHB_CompanyOwnerSerializer, {"many": False}),
            "employees": (DHB_CompanyEmployeesSerializer, {"many": True}),
            "addresses": (DHB_CompanyAddressesSerializer, {"many": True}),
        }
