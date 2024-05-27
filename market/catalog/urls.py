from django.urls import path

import catalog.views

app_name = "catalog"

urlpatterns = [
    path("", catalog.views.item_list, name="item_list"),
    path("<int:pk>/", catalog.views.item_detail, name="item_detail"),
    path("add_to_cart/", catalog.views.add_to_cart, name="add_to_cart"),
    path(
        "favorite_toggle/",
        catalog.views.favorite_toggle,
        name="favorite_toggle",
    ),
    path(
        "favorite_remove/<int:pk>/",
        catalog.views.favorite_remove,
        name="favorite_remove",
    ),
]
