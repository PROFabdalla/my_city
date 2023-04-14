from django.urls import include, path


urlpatterns = [
    # ---------------------- APPS --------------------------- #
    path("company/", include("public_apps.company.urls")),
]
