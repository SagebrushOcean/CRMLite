from django.contrib import admin
from . import models

@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['INN', 'title']

@admin.register(models.Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ['address', 'company_id']

@admin.register(models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['INN', 'title']

class SupplyProductInline(admin.TabularInline):
    model = models.SupplyProduct
    extra = 0

@admin.register(models.Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'delivery_date', 'supplier_id']
    list_display_links = ('id', 'delivery_date')
    inlines = [SupplyProductInline]

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'quantity', 'storage_id', 'created_at','updated_at','purchase_price','sale_price']

