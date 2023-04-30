from django.urls import include, path

urlpatterns = [
    # ---------------------- APPS --------------------------- #
    path("users/", include("site_admin.membership.users.urls")),
    path("company/", include("site_admin.membership.companies.urls")),
]
