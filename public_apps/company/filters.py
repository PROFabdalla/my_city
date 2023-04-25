from django_filters import rest_framework as filters

from public_apps.company.models import Company


class CompanyFilter(filters.FilterSet):
    find = filters.CharFilter(method="custom_search", label="Search")

    class Meta:
        model = Company
        fields = ("role", "active", "find")

    def custom_search(self, queryset, name, value):
        return queryset.filter(title__icontains=value)
