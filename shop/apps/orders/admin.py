from django.contrib import admin
from .models import Order, OrderDetails

class OrderDetailsInline(admin.TabularInline):
    model = OrderDetails
    extra = 3


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('Customer', 'register_date', 'is_finaly', 'discount')
    inlines = [OrderDetailsInline]

