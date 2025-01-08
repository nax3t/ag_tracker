from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'unit', 'cost_per_unit', 'location', 'user']
    list_filter = ['category', 'unit', 'user']
    search_fields = ['name', 'description', 'location', 'supplier']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category', 'user')
        }),
        ('Inventory Details', {
            'fields': ('quantity', 'unit', 'cost_per_unit', 'minimum_stock')
        }),
        ('Additional Information', {
            'fields': ('expiry_date', 'supplier')
        }),
        ('Location Information', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ) 