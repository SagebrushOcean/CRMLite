from django.contrib import admin
from . import models

@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['INN', 'title']


@admin.register(models.Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ['address', 'company_id']

# @admin.register(models.Supplier)
# class SupplierAdmin(admin.ModelAdmin):
#     list_display = ['INN', 'title']
#
# @admin.register(models.Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['storage_id', 'title']