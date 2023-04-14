from public_apps.company.models import Company
from core.utils import CustomFieldsModelSerializer


class CompanySerializer(CustomFieldsModelSerializer):
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
        )
