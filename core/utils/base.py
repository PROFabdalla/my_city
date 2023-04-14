from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.serializers import CountryFieldMixin
from hashid_field import HashidAutoField, HashidField
from hashid_field.rest import HashidSerializerCharField


class BaseModel(models.Model):
    id = HashidAutoField(primary_key=True)
    created_at = models.DateTimeField(
        _("created"), editable=False, auto_now_add=True, blank=True
    )
    updated_at = models.DateTimeField(
        _("modified"), editable=False, auto_now=True, blank=True
    )
    active = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        abstract = (
            True  # ! this model is subclassed by other models that inherit its fields
        )
        ordering = ["-id"]


class CustomFlexFieldsModelSerializer(CountryFieldMixin, FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)
