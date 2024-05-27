from django.shortcuts import render, redirect
from django.urls import reverse
import catalog.models
from catalog.models import CartItem, OrderHistory
from django.utils.crypto import get_random_string

__all__ = ["profile", "cart", "home"]


def profile(request):
    user = request.user
    orders = OrderHistory.objects.filter(user=request.user).order_by('-order_date')
    context = {"user": user,
               'orders': orders}
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

def checkout_view(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.item.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        full_name = request.POST['full_name']
        address = request.POST['address']
        phone_number = request.POST['phone_number']

        items = ', '.join([f'{item.item.name} (x{item.quantity})' for item in cart_items])
        order_number = get_random_string(length=12).upper()
        order = OrderHistory.objects.create(
            user=user,
            order_number=order_number,
            items=items,
            total_price=total_price
        )

        CartItem.objects.filter(cart__user=user).delete()

        return redirect(f"https://www.tinkoff.ru/rm/kruglov.egor19/ZZNz358951?moneyAmount={total_price}")
    return render(request, 'homepage/checkout.html')