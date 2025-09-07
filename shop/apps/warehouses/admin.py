from django.contrib import admin

# Register your models here.

from .models import Warehouse,WarehouseType

class WarehouseAdmininlines(admin.TabularInline):
    model = Warehouse

@admin.register(WarehouseType)
class WarehouseTypeAdmin(admin.ModelAdmin):
    list_display = ('id','warehouse_type_title',)
    
    inlines = [WarehouseAdmininlines]
 

@admin.register(Warehouse)   
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('product','price','qty','warehouse_type','register_date')
    