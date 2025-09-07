from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.products.models import Product
#---------------------------------------------------------------------------------------------------------------------------
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10, unique=True,verbose_name="کد کوپن")
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    end_data = models.DateTimeField(verbose_name="تاریخ پایان")
    discount = models.IntegerField(verbose_name="درصد تخفیف",validators=[MinValueValidator(0),MaxValueValidator(100)])
    is_active = models.BooleanField(default=False,verbose_name="وضعیت فعال بودن یا نبود")
    
    class Meta:
        verbose_name = "کوپن تخفیف"
        verbose_name_plural = "کوپن ها"
    
    def __str__(self):
        return self.coupon_code
#---------------------------------------------------------------------------------------------------------------------------
class DiscountBasket(models.Model):
    discount_title = models.CharField(max_length=100,verbose_name="عنوان سب تخفیف")
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    end_data = models.DateTimeField(verbose_name="تاریخ پایان")
    discount = models.IntegerField(verbose_name="درصد تخفیف",validators=[MinValueValidator(0),MaxValueValidator(100)])
    is_active = models.BooleanField(default=False,verbose_name="وضعیت فعال بودن یا نبود")
    
    class Meta:
        verbose_name = "سبد تخفیف"
        verbose_name_plural = "سبد های تخفیف"
    
    def __str__(self):
        return self.discount_title
#---------------------------------------------------------------------------------------------------------------------------
class DiscountBasketDetails(models.Model):
    discount_basket = models.ForeignKey(DiscountBasket,on_delete=models.CASCADE,verbose_name="سبد تخفیف",related_name="discount_basket_details")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="کالا",related_name="discount_basket_details_product")
    class Meta:
        verbose_name = "جزییات سبد تخفیف"