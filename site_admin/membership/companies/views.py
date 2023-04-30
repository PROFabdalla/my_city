from public_apps.company.models import Company
from rest_framework import generics
from public_apps.company.filters import CompanyFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from site_admin.membership.companies.serializers.company import AD_CompanySerializer
from django.db.models import Q
from rest_framework.response import Response


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.filter(~Q(title="owner"))
    serializer_class = AD_CompanySerializer
    filterset_class = CompanyFilter
    permission_classes = [IsAuthenticated & IsAdminUser]


class CompanyOverView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.filter(~Q(title="owner"))
    serializer_class = AD_CompanySerializer
    filterset_class = CompanyFilter
    permission_classes = [IsAuthenticated & IsAdminUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            fields=[
                "active",
            ],
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
