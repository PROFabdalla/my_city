from django.urls import include, path
from rest_framework.routers import DefaultRouter
from allauth.account.views import LoginView as SocialLogoutView

from user_app.views import CustomLoginView, CustomUserViewSet, LogoutAllView, LogoutView

app_name = "user_app"


router = DefaultRouter()
router.register("users", CustomUserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", CustomLoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("logoutall/", LogoutAllView.as_view()),
    # --------------------- social logout ---------------- #
    path("accounts/logout/", SocialLogoutView.as_view(), name="account_logout"),
]
