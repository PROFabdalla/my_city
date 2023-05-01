from django.db import models

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from core.utils.base import BaseModel
from core.validators import (
    ZipCodeValidator,
)
from public_apps.company.models import Company
from user_app.models import User


class Addresses(BaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="addresses",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="addresses", null=True, blank=True
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
