from django.db import models


class CompanyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
