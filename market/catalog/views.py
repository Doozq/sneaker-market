from django.shortcuts import get_object_or_404, render

import catalog.models

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
