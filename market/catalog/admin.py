from django.contrib import admin
from django.utils.html import mark_safe

import catalog.models

__all__ = ["GalleryImageInLine", "MainImageInLine", "ItemAdmin"]


admin.site.register(catalog.models.Tag)
admin.site.register(catalog.models.Category)


class GalleryImageInLine(admin.TabularInline):
    verbose_name = "изображение галереи"
    verbose_name_plural = "изображения галереи"
    model = catalog.models.GalleryImage
    fields = ("image",)


class MainImageInLine(admin.TabularInline):
    verbose_name = "Главное изображение"
    model = catalog.models.MainImage
    fields = ("image",)


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.main_image_tmb,
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    inlines = [MainImageInLine, GalleryImageInLine]
    readonly_fields = (
        catalog.models.Item.main_image_tmb,
        "admin_gallery",
    )

    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)

    filter_horizontal = (catalog.models.Item.tags.field.name,)

    def admin_gallery(self, obj):
        urls = obj.get_gallery_urls()
        if urls:
            html_template = (
                "<div style='border: solid 3px grey; "
                "width: 932px; padding: 5px 6px;'>\n"
            )
            for image_url in urls:
                html_template += (
                    f"  <img src='{image_url}' style='margin: 5px 4px;'>\n"
                )
            html_template += "</div>"
            return mark_safe(html_template)
        return mark_safe("<p>Нет избражений</p>")

    admin_gallery.short_description = "Галлерея"


class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'order_date', 'total_price')
    list_filter = ('order_date', 'user')
    search_fields = ('order_number', 'user__username', 'items')

admin.site.register(catalog.models.OrderHistory, OrderHistoryAdmin)


@admin.register(catalog.models.FavoriteItem)
class FavoriteItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item')
    list_filter = ('user', 'item')
    search_fields = ('user__username', 'item__name')