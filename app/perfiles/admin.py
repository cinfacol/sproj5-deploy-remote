from django.contrib import admin

from .models import Address, Profile, UserBase

admin.site.register(UserBase, list_display=(
    'username',
    'email',
    'first_name',
    'last_name',
))
admin.site.register(Address, list_display=(
    'user',
    'shipping_address',
    'billing_address',
    'address_type',
    'default',
))

admin.site.register(Profile, list_display=(
    'user',
    'picture',
    'phone',
    'bio',
    'verified',
))
