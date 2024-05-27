from django.contrib import auth
from django.urls import path

import users.views

app_name = "users"

urlpatterns = [
    path(
        "login/",
        auth.views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("logout/", auth.views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        auth.views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth.views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path("signup/", users.views.signup, name="signup"),
    path("users/", users.views.user_list, name="user_list"),
    path("users/<int:pk>/", users.views.user_detail, name="user_detail"),
    path("profile/", users.views.profile, name="profile"),
]
