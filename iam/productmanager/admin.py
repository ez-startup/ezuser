from django.contrib import admin
from .models import *

# Register your models here.
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'created_date', 'updated_date')
    search_fields = ('type_name',)
    
admin.site.register(ProductType, ProductTypeAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_type', 'is_active', 'created_date', 'updated_date')
    list_filter = ('product_type', 'is_active')
    search_fields = ('product_name', 'product_description')
    
admin.site.register(Product, ProductAdmin)


class LicenseAdmin(admin.ModelAdmin):
    list_display = ('license_type', 'product_key', 'number', 'valid_date', 'expired_date', 'product_id', 'created_date', 'updated_date')
    list_filter = ('license_type', 'valid_date', 'expired_date', 'product_id')
    search_fields = ('license_type', 'product_id__product_name')
    
admin.site.register(License, LicenseAdmin)

   
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'ip_address', 'mac_address', 'license_id', 'created_date', 'updated_date')
    list_filter = ('license_id', 'created_date', 'updated_date')
    search_fields = ('device_name', 'ip_address', 'mac_address')

admin.site.register(Device, DeviceAdmin)