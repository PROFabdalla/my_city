from django_filters import rest_framework as filters
from user_app.models import User


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ("is_admin", "is_active")
