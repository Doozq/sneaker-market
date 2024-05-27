from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
import catalog.models
from catalog.models import Cart, CartItem
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
    quantity = 1  # Default quantity to 1 as per the single button functionality

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return JsonResponse({'status': 'success'})