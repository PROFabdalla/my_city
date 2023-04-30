from django.urls import path
from site_admin.membership.companies.views import CompanyListView, CompanyOverView

urlpatterns = [
    # ---------------------- APPS --------------------------- #
    path("", CompanyListView.as_view(), name="companies"),
    path("overview/<str:pk>/", CompanyOverView.as_view(), name="company_overView"),
]
