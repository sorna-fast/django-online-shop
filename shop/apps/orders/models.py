from django.db import models
from apps.accounts.models import Customer
from apps.products.models import Product
from django.utils import timezone
import uuid
import utils
#______________________________________________________________________________________________________________________________
class PaymentType(models.Model):
    payment_title = models.CharField(max_length=32, verbose_name='نوع روش پرداخت')
    def __str__(self):
        return self.payment_title
    class Meta:
        verbose_name='نوع روش پرداخت'
        verbose_name_plural='نوع روش های پرداخت'

#______________________________________________________________________________________________________________________________

class Order(models.Model):
    Customer=models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='orders', verbose_name='مشتری')
    register_date=models.DateField(default=timezone.now,verbose_name='تاریخ درج سفارس')
    update_date=models.DateField(auto_now=True, verbose_name='تاریخ ویرایش سفارس')
    is_finaly=models.BooleanField(default=True, verbose_name='وضعیت پرداخت')
    oder_code=models.CharField(max_length=36,default=uuid.uuid4,unique=True,editable=False,verbose_name='کد تولیدی برای سفارش')
    discount=models.IntegerField(blank=True,null=True,default=0,verbose_name='تخفیف روی فاکتور')
    description=models.TextField(blank=True,null=True,verbose_name='توضیحات')
    payment = models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=True,blank=True,related_name='pyman_types', verbose_name='نوع روش پرداخت')
    def get_order_total_price(self):
        sum_=0
        for item in self.order_details1.all():
            sum_+=item.product.get_price_by_discount()*item.quantity
        order_final_price,delivery,tax=utils.price_by_delivery_tax(sum_,self.discount)
        return int((order_final_price)*10)

    def __str__(self):
        return f'{self.Customer}\t{self.id}\t{self.is_finaly}'
    class Meta:
        verbose_name='سفارش'
        verbose_name_plural='سفارشات'
#______________________________________________________________________________________________________________________________

class OrderDetails(models.Model):
    Order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details1', verbose_name='سفارش')
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_details2', verbose_name='کالا')
    quantity=models.PositiveIntegerField(default=1,verbose_name='تعداد محصول')
    price=models.IntegerField(verbose_name='قیمت محصول')
    def __str__(self):
        return f'{self.Product}\t{self.price}\t{self.quantity}'
    class Meta:
        verbose_name='جزییات سفارش'
        verbose_name_plural='جزییات سفارشات'