from django.urls import path

import homepage.views

app_name = "homepage"

urlpatterns = [
    path("", homepage.views.home, name="home"),
    path("profile/", homepage.views.profile, name="profile"),
    path("cart/", homepage.views.cart_view, name="cart"),
    path("checkout/", homepage.views.checkout_view, name="checkout"),
]
