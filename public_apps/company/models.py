from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from core.utils.base import BaseModel
from public_apps.company.managers import CompanyManager
from public_apps.company.utils import PhoneNumberValidator, ZipCodeValidator

ROLES = (
    ("internal", "internal"),
    ("external", "external"),
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
    role = models.CharField(choices=ROLES, max_length=25)
    objects = CompanyManager()

    def __str__(self):
        return self.title


class CompanyAddresses(BaseModel):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="addresses"
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

    def __str__(self):
        return f"{self.country}/{self.city}"
