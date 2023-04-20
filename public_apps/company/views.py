from rest_framework import generics
from public_apps.company.models import Company
from public_apps.company.serializers.company import CompanySerializer
from public_apps.company.filters import CompanyFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.filter(Q(active=True), ~Q(title="owner"))
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter
    permission_classes = [IsAuthenticated]
