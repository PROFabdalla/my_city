from django.db import models
from core.utils.base import BaseModel


class Employee(BaseModel):
    EMPLOYEE_ROLE = (
        ("admin", "admin"),
        # TODO employee must choose only this choices blow
        ("employee", "employee"),
        ("vendors", "vendors"),
        ("sponsor", "sponsor"),
    )
    user = models.OneToOneField(
        "user_app.User",
        on_delete=models.CASCADE,
        verbose_name=("The User"),
        related_name="employee",
    )
    company = models.ForeignKey(
        "public_apps.Company",
        related_name="employee",
        on_delete=models.CASCADE,
    )
    role = models.CharField(choices=EMPLOYEE_ROLE, max_length=25)
    position = models.CharField(max_length=120)

    def __str__(self):
        return self.user.username
