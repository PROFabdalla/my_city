from user_app.models import User
from rest_framework import generics
from user_app.filters import UserFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from site_admin.membership.users.serializers.users import AD_UserActivationSerializer
from django.db.models import Q
from rest_framework.response import Response


class UsersListView(generics.ListAPIView):
    serializer_class = AD_UserActivationSerializer
    filterset_class = UserFilter
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get_queryset(self):
        queryset = User.objects.filter(~Q(email=self.request.user.email))
        return queryset


class UsersOverView(generics.RetrieveUpdateAPIView):
    serializer_class = AD_UserActivationSerializer
    filterset_class = UserFilter
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get_queryset(self):
        queryset = User.objects.filter(~Q(email=self.request.user.email))
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            fields=[
                "is_active",
            ],
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
