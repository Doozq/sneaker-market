from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
import catalog.models
from catalog.models import Cart, CartItem, Item
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

__all__ = ["item_detail", "item_list"]


def item_list(request):
    items = catalog.models.Item.objects.published()
    template = "catalog/item_list.html"
    context = {"items": items}
    return render(request, template, context)


def item_detail(request, pk):
    queryset = catalog.models.Item.objects.queryset_for_item_detail()
    item = get_object_or_404(queryset, pk=pk)
    template = "catalog/item.html"
    context = {"item": item}
    return render(request, template, context)

@login_required
@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = 1 

    product = get_object_or_404(Item, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=product)
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect(request.META.get('HTTP_REFERER'))