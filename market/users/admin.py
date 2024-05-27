from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from users.models import Profile
from catalog.models import Cart, CartItem  

__all__ = ["ProfileInline", "UserAdmin", "CartAdmin", "CartItemAdmin"]

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# Custom admin classes for Cart and CartItem
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = (CartItemInline,)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product_id', 'quantity', 'added_at')


# Register the new models with the admin site
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
