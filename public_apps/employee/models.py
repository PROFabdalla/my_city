from django.db import models

from core.utils.base import BaseModel
from core.validators import PhoneNumberValidator
from django.utils.translation import gettext_lazy as _


class Employee(BaseModel):
    EMPLOYEE_ROLE = (
        ("admin", "admin"),
        # TODO employee must choose only this choices blow
        ("factory_admin", "factory_admin"),
        ("club_admin", "club_admin"),
        ("vendors", "vendors"),
        ("sponsor", "sponsor"),
        ("employee", "employee"),
    )
    user = models.OneToOneField(
        "user_app.User",
        on_delete=models.CASCADE,
        verbose_name=("The User"),
        related_name="employee",
    )
    company = models.ForeignKey(
        "public_apps.Company",
        related_name="employees",
        on_delete=models.CASCADE,
    )
    phone_number = models.CharField(
        max_length=12,
        verbose_name=("Phone Number"),
        validators=[PhoneNumberValidator],
    )
    role = models.CharField(choices=EMPLOYEE_ROLE, max_length=25)
    position = models.CharField(max_length=120)

    def __str__(self):
        return self.user.username


class Permissions(BaseModel):
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        verbose_name=_("Employee"),
        related_name="permissions",
    )
    company_admin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.employee.user.username)
