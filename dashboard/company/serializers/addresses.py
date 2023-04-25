from hashid_field import HashidField
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from core.utils.base import CustomModelSerializer
from public_apps.company.models import Company, CompanyAddresses


class DHB_CompanyAddressesSerializer(CustomModelSerializer):
    company = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        many=False,
        required=False,
        read_only=True,
    )

    class Meta:
        model = CompanyAddresses
        fields = (
            "id",
            "company",
            "country",
            "city",
            "address_line",
            "zip",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data.update(company=user.employee.company)
        return super().create(validated_data)
