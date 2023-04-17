from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from core.utils.base import BaseModel
from public_apps.company.managers import CompanyManager
from public_apps.company.utils import PhoneNumberValidator, ZipCodeValidator

ROLES = (
    ("internal", "internal"),
    ("3rd Party", "3rd Party"),
)


class Company(BaseModel):
    title = models.CharField(max_length=144, verbose_name=_("title"))
    owner = models.OneToOneField(
        "user_app.User",
        on_delete=models.CASCADE,
        related_name="company",
    )
    business_description = models.TextField(verbose_name=_("Business Description"))
    phone_number = models.CharField(
        max_length=12,
        verbose_name=("Phone Number"),
        validators=[PhoneNumberValidator],
    )
    country = CountryField(
        blank_label="select country",
        verbose_name=("Country"),
    )
    city = models.CharField(max_length=40, verbose_name=_("City"))
    address_line = models.CharField(max_length=144, verbose_name=("address line"))

    zip = models.CharField(
        max_length=144,
        validators=[
            ZipCodeValidator,
        ],
        null=True,
        blank=True,
        verbose_name=("Zip Code"),
    )
    role = models.CharField(choices=ROLES, default="3rd Party", max_length=25)
    objects = CompanyManager()
