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
    path(
        "password_reset/",
        auth.views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth.views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth.views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth.views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path("signup/", users.views.signup, name="signup"),
    path("activate/<str:username>/", users.views.activate, name="activate"),
    path("users/", users.views.user_list, name="user_list"),
    path("users/<int:pk>/", users.views.user_detail, name="user_detail"),
    path("profile/", users.views.profile, name="profile"),
]
