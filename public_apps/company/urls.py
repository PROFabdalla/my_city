from django.urls import path

from public_apps.company.views import CompanyListView

urlpatterns = [
    # ---------------------- APPS --------------------------- #
    path("", CompanyListView.as_view(), name="companies"),
]
