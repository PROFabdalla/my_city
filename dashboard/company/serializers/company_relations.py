from core.utils.base import CustomModelSerializer
from public_apps.employee.models import Employee
from public_apps.company.models import CompanyAddresses

from user_app.models import User


class CompanyOwnerSerializer(CustomModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class CompanyEmployeesSerializer(CustomModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "user", "position")


class CompanyAddressesSerializer(CustomModelSerializer):
    class Meta:
        model = CompanyAddresses
        fields = ("id", "country", "city", "address_line", "zip")
