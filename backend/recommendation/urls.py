from django.urls import path

from recommendation.views import UserRegisterView, UserLoginView, UserLogoutView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
]
