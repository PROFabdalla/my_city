from rest_framework import generics
from public_apps.company.models import Company
from public_apps.company.serializers.company import CompanySerializer
from public_apps.company.filters import CompanyFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.filter(role="3rd Party", active=True)
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.request.user, "--------------")
        return super().get_queryset()
