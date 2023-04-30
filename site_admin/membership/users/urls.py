from django.urls import path
from site_admin.membership.users.views import UsersListView, UsersOverView

urlpatterns = [
    # ---------------------- APPS --------------------------- #
    path("", UsersListView.as_view(), name="users"),
    path("overview/<str:pk>/", UsersOverView.as_view(), name="users_overView"),
]
