from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils.base import BaseModel
from public_apps.company.managers import CompanyManager
from core.validators import (
    PhoneNumberValidator,
    validate_file_extension,
)

ROLES = (
    ("internal", "internal"),
    ("external", "external"),
)


class Company(BaseModel):
    owner = models.OneToOneField(
        "user_app.User",
        on_delete=models.CASCADE,
        related_name="company",
    )
    title = models.CharField(max_length=144, verbose_name=_("title"))
    email = models.EmailField(
        max_length=144, verbose_name="Company Email", null=True, blank=True
    )
    business_description = models.TextField(verbose_name=_("Business Description"))
    phone_number = models.CharField(
        max_length=12,
        verbose_name=("Phone Number"),
        validators=[PhoneNumberValidator],
    )
    Website = models.CharField(
        max_length=144, verbose_name=("Website"), null=True, blank=True
    )
    tax_file = models.FileField(
        null=True, blank=True, validators=[validate_file_extension]
    )
    role = models.CharField(choices=ROLES, max_length=25)
    objects = CompanyManager()

    def __str__(self):
        return self.title
