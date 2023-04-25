from django.urls import include, path

urlpatterns = [
    # ---------------------- APPS --------------------------- #
    path("company/", include("dashboard.company.urls")),
]
