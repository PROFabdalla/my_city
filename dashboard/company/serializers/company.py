from core.utils.base import CustomModelSerializer
from public_apps.company.models import Company, CompanyAddresses
from dashboard.company.serializers.company_relations import (
    CompanyEmployeesSerializer,
    CompanyOwnerSerializer,
    CompanyAddressesSerializer,
)
from hashid_field import HashidField
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers


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
        queryset=CompanyAddresses.objects.all(),
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
            "owner": (CompanyOwnerSerializer, {"many": False}),
            "employees": (CompanyEmployeesSerializer, {"many": True}),
            "addresses": (CompanyAddressesSerializer, {"many": True}),
        }
