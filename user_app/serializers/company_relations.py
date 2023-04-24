from core.utils.base import CustomModelSerializer
from public_apps.company.models import Company
from public_apps.employee.models import Employee
from hashid_field import HashidField
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers


class UserCompanySerializer(CustomModelSerializer):
    class Meta:
        model = Company
        fields = (
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
        extra_kwargs = {
            "owner": {"read_only": True, "required": False},
            "role": {"read_only": False, "required": True},
        }


# ----------- employee in company ----------------------- #
class UserEmployeeSerializer(CustomModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        many=False,
        required=False,
        read_only=True,
    )
    company = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        many=False,
        required=False,
        read_only=True,
    )
    role = serializers.ChoiceField(
        choices=(
            ("factory_admin", "factory_admin"),
            ("club_admin", "club_admin"),
            ("vendors", "vendors"),
            ("sponsor", "sponsor"),
            ("employee", "employee"),
        ),
        required=True,
    )

    class Meta:
        model = Employee
        fields = ("id", "user", "phone_number", "role", "company", "position")
        extra_kwargs = {
            "user": {"read_only": True, "required": False},
            "company": {"read_only": True, "required": False},
        }


# ----------------- employee if create new company ----------------- #
class UserEmployeeAdminSerializer(CustomModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        many=False,
        required=False,
        read_only=True,
    )
    company = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        many=False,
        required=False,
        read_only=True,
    )
    role = serializers.ChoiceField(
        choices=(
            ("vendors", "vendors"),
            ("sponsor", "sponsor"),
        ),
        required=True,
    )

    class Meta:
        model = Employee
        fields = ("id", "user", "phone_number", "role", "company", "position")
        extra_kwargs = {
            "user": {"read_only": True, "required": False},
            "company": {"read_only": True, "required": False},
        }
