from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (Attribute, AttributeValue, Brand, Category, Media,
                     Product, Type)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'attribute_value']


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [
        AttributeValueInline,
    ]
    list_display = ['name', 'description']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'id', 'slug', 'is_active']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'alt_text', 'image', 'created_at', 'default']


class MediaInline(admin.TabularInline):
    model = Media


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        MediaInline,
    ]

    list_display = ['name', 'slug', 'brand',
                    'store_price', 'percent_discount_price', 'discount_price', 'get_categories']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
