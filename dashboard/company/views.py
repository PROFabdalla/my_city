from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from dashboard.company.serializers.addresses import DHB_CompanyAddressesSerializer
from dashboard.company.serializers.company import DHB_CompanySerializer
from public_apps.company.filters import CompanyFilter
from public_apps.company.models import Company
from public_apps.addresses.models import Addresses
from user_app.permissions import IsCompanyAdmin, IsEmployee


class DHB_CompanyListView(generics.ListAPIView):
    serializer_class = DHB_CompanySerializer
    filterset_class = CompanyFilter
    permission_classes = [IsAuthenticated & IsEmployee]

    def get_queryset(self):
        user = self.request.user
        queryset = Company.objects.filter(active=True, pk=user.employee.company.id)
        return queryset


class DHB_CompanyOverview(generics.RetrieveUpdateAPIView):
    serializer_class = DHB_CompanySerializer
    filterset_class = CompanyFilter
    permission_classes = [IsAuthenticated & IsCompanyAdmin]

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated & IsEmployee]
        else:
            permission_classes = [IsAuthenticated & IsCompanyAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = Company.objects.filter(active=True, pk=user.employee.company.id)
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            # update in only this fields
            fields=["title", "business_description", "phone_number"],
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


# --------------------- company Addresses -------------------- #
class DHB_CompanyAddressesListView(generics.ListCreateAPIView):
    serializer_class = DHB_CompanyAddressesSerializer
    permission_classes = [IsAuthenticated & IsEmployee]

    def get_queryset(self):
        user = self.request.user
        queryset = Addresses.objects.filter(company=user.employee.company)
        return queryset


class DHB_CompanyAddressesOverview(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DHB_CompanyAddressesSerializer
    permission_classes = [IsAuthenticated & IsEmployee]

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated & IsEmployee]
        else:
            permission_classes = [IsAuthenticated & IsCompanyAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = Addresses.objects.filter(company=user.employee.company)
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            # update in only this fields
            fields=["country", "city", "address_line", "zip"],
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
