from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
import catalog.models
from catalog.models import Cart, CartItem, Item, FavoriteItem
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import logging

__all__ = ["item_detail", "item_list"]


def item_list(request):
    items = catalog.models.Item.objects.published()

    model = request.GET.get('model')
    brand = request.GET.get('brand')
    color = request.GET.getlist('color')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    is_search = any((model, brand, color, price_min, price_max))
    if model:
        items = items.filter(name__icontains=model)
    if brand:
        items = items.filter(category__name__icontains=brand)
    if color:
        items = items.filter(color__in=color)
    if price_min:
        items = items.filter(price__gte=price_min)
    if price_max:
        items = items.filter(price__lte=price_max)

    favorite_item = request.user.favorite_items.all() if request.user.is_authenticated else []
    favorite_items = [item.item for item in favorite_item]    
    template = "catalog/item_list.html"
    context = {"items": items, "is_search": is_search,
               'favorite_items': favorite_items,}
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


@csrf_exempt
@require_POST
def favorite_toggle(request):

    data = json.loads(request.body)
    item_id = data.get('item_id')
    user = request.user

    item = Item.objects.get(pk=item_id)

    favorite_item, created = FavoriteItem.objects.get_or_create(user=user, item=item)

    if created:
        return JsonResponse({'status': 'added'})
    else:
        favorite_item.delete()
        return JsonResponse({'status': 'removed'})
    
    
@login_required
def favorite_remove(request, pk):
    item = get_object_or_404(Item, pk=pk)
    favorite_item = FavoriteItem.objects.filter(user=request.user, item=item).first()
    if favorite_item:
        favorite_item.delete()
    return redirect('users:profile')    
