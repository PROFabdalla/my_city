from django.db import models
from django.utils.translation import gettext_lazy as _
from core.utils.base import BaseModel
from public_apps.factory.managers import FactoryManager
from core.validators import validate_file_extension, PhoneNumberValidator


class Factory(BaseModel):
    title = models.CharField(max_length=144, verbose_name=_("title"))
    owner = models.OneToOneField(
        "public_apps.Employee",
        on_delete=models.CASCADE,
        related_name="factory",
    )
    company = models.ForeignKey(
        "public_apps.Company",
        on_delete=models.CASCADE,
        related_name="factory",
    )
    phone_number = models.CharField(
        max_length=12,
        verbose_name=("Phone Number"),
        validators=[PhoneNumberValidator],
    )
    commercial_file = models.FileField(
        null=True, blank=True, validators=[validate_file_extension]
    )
    employee_num = models.PositiveIntegerField()
    objects = FactoryManager()

    def __str__(self):
        return self.title
