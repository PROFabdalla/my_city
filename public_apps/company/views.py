from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from public_apps.company.filters import CompanyFilter
from public_apps.company.models import Company
from public_apps.company.serializers.company import CompanySerializer


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.filter(Q(active=True), ~Q(title="owner"))
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter
    permission_classes = [IsAuthenticated]
