from core.utils.base import CustomModelSerializer
from public_apps.addresses.models import Addresses
from public_apps.employee.models import Employee
from user_app.models import User


class DHB_CompanyOwnerSerializer(CustomModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class DHB_CompanyEmployeesSerializer(CustomModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "user", "position")


class DHB_CompanyAddressesSerializer(CustomModelSerializer):
    class Meta:
        model = Addresses
        fields = ("id", "country", "city", "address_line", "zip")
