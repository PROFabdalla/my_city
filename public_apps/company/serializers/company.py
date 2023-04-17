from core.utils.base import CustomModelSerializer
from public_apps.company.models import Company
from user_app.models import User


class UserSerializer(CustomModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


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
        )

        expandable_fields = {
            "owner": (UserSerializer, {"many": False}),
        }
