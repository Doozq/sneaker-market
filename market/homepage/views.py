from django.shortcuts import render

import catalog.models


__all__ = ["profile", "cart", "home"]


def profile(request):
    template = "homepage/profile.html"
    return render(request, template)


def cart(request):
    items = catalog.models.Item.objects.on_main()
    template = "homepage/cart.html"
    context = {"items": items}
    return render(request, template, context)


def home(request):
    items = catalog.models.Item.objects.on_main()
    template = "homepage/main.html"
    context = {"items": items}
    return render(request, template, context)
