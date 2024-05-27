from django.shortcuts import render

import catalog.models
from catalog.models import CartItem

__all__ = ["profile", "cart", "home"]


def profile(request):
    user = request.user
    context = {"user": user}
    template = "homepage/profile.html"
    return render(request, template, context)


def cart(request):
    items = catalog.models.Item.objects.on_main()
    template = "homepage/cart.html"
    context = {"items": items}
    return render(request, template, context)


def cart_view(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.item.price * item.quantity for item in cart_items)
    template = "homepage/cart.html"
    context = {
        'items': cart_items,
        'total_price': total_price,
        "user": user
    }
    return render(request, template, context)


def home(request):
    items = catalog.models.Item.objects.on_main()
    template = "homepage/main.html"
    context = {"items": items}
    return render(request, template, context)
