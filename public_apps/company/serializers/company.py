from core.utils.base import CustomModelSerializer
from public_apps.company.models import Company
from public_apps.company.serializers.company_relations import (
    CompanyEmployeesSerializer,
    CompanyOwnerSerializer,
)


class CompanySerializer(CustomModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "title",
            "owner",
            "business_description",
            "phone_number",
            "country",
            "city",
            "address_line",
            "zip",
            "role",
            "employee",
        )

        expandable_fields = {
            "owner": (CompanyOwnerSerializer, {"many": False}),
            "employee": (CompanyEmployeesSerializer, {"many": True}),
        }
