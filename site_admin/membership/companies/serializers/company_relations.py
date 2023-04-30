from core.utils.base import CustomModelSerializer
from public_apps.employee.models import Employee
from user_app.models import User


class AD_CompanyOwnerSerializer(CustomModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class AD_CompanyEmployeesSerializer(CustomModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "user", "position")
