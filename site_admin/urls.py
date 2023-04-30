from django.urls import include, path

urlpatterns = [
    # ---------------------- APPS --------------------------- #
    path("membership/", include("site_admin.membership.urls")),
]
