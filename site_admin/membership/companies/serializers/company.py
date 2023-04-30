from hashid_field import HashidField
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from core.utils.base import CustomModelSerializer
from public_apps.company.models import Company
from site_admin.membership.companies.serializers.company_relations import (
    AD_CompanyOwnerSerializer,
    AD_CompanyEmployeesSerializer,
)


class AD_CompanySerializer(CustomModelSerializer):
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

    class Meta:
        model = Company
        fields = (
            "id",
            "active",
            "title",
            "owner",
            "business_description",
            "phone_number",
            "role",
            "employees",
        )

        expandable_fields = {
            "owner": (AD_CompanyOwnerSerializer, {"many": False}),
            "employees": (AD_CompanyEmployeesSerializer, {"many": True}),
        }
