from django.contrib import admin

from .models import Inventory, Stock


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['sku', 'upc', 'created_at']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['inventory', 'units', 'units_sold']
