from django.urls import path
from dashboard.company.views import (
    DHB_CompanyListView,
    DHB_CompanyOverview,
    DHB_CompanyAddressesListView,
    DHB_CompanyAddressesOverview,
)

urlpatterns = [
    # ---------------------- APPS --------------------------- #
    path("", DHB_CompanyListView.as_view(), name="company"),
    path("overview/<str:pk>/", DHB_CompanyOverview.as_view(), name="company_overview"),
    # ---------------- addresses ---------------------- #
    path(
        "addresses/", DHB_CompanyAddressesListView.as_view(), name="company_addresses"
    ),
    path(
        "addresses/overview/<str:pk>/",
        DHB_CompanyAddressesOverview.as_view(),
        name="company_addresses_overview",
    ),
]
