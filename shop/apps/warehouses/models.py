from django.db import models

# Create your models here.

from apps.products.models import Product
from apps.accounts.models import CustomUser
# -----------------------------------------------------------------------------------------------

class WarehouseType(models.Model):
    warehouse_type_title = models.CharField(max_length=50,verbose_name='نوع انبار')
    
    def __str__(self):
        return self.warehouse_type_title
    
    class Meta:
        verbose_name = 'نوع انبار'
        verbose_name_plural = 'انواع انبار'

# -----------------------------------------------------------------------------------------------

# از نظر نوع یوزر مدیر یا اپراتور کالا رو به سیستم وارد و مشتری کالا رو خارج میکند
# auto_now_add : دقیقا تاریخ خروج و ورود ثبت میشه

class Warehouse(models.Model):
    warehouse_type = models.ForeignKey(WarehouseType,on_delete=models.CASCADE,verbose_name='نوع انبار',related_name='warehouses')
    user_registered = models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر انباردار',related_name='warehouseuser_registered')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='warehouse_products')
    qty = models.IntegerField(verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت',null=True,blank=True)
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت')

    def __str__(self):
        return f"{self.warehouse_type} - {self.product}"

    class Meta:
        verbose_name = 'انبار'
        verbose_name_plural = 'انبار ها'