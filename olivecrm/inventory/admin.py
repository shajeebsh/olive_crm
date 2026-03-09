from django.contrib import admin
from .models import Product, Warehouse, StockLevel

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'is_active')
    search_fields = ('name', 'sku')

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

@admin.register(StockLevel)
class StockLevelAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity', 'reorder_level')
    list_filter = ('warehouse',)
