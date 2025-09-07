from django.contrib import admin
from .models import Coupon, DiscountBasket, DiscountBasketDetails

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code', 'discount', 'is_active', 'start_date', 'end_data']

class DiscountBasketAdminInline(admin.TabularInline):
    model = DiscountBasketDetails
    fields = ['product']  # نمایش فیلد product در اینلاین
    extra = 3

@admin.register(DiscountBasket)
class DiscountBasketAdmin(admin.ModelAdmin):
    list_display = ['discount_title', 'start_date', 'end_data', 'discount', 'is_active']
    inlines = [DiscountBasketAdminInline]  # استفاده از لیست به جای تاپل