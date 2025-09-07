# لیست سیگنال هایی که میشه در پروژه جنگو استفاده کرد رو میشه توی گوگل سرچ کرد
# انفاقاتی که بعد یک اکشنی رخ میده
# هر وقت واسه اپی سیگنال نوشتی برو تو اپسش و تابع ردی رو اضاف کن

from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Product
from django.conf import settings
import os

# kwargs['instance'] : اشاره داره به کل رکوردی که برای حذف انتخاب شده
@receiver(post_delete,sender=Product)
def delete_product_image(sender,**kwargs):
    # این تکه کد ادرس عکسی که واسه حذف انتخاب کردی رو پیدا و از سیستم سرور حذفش میکنه
    path = settings.MEDIA_ROOT + str(kwargs['instance'].image_name)
    if os.path.isfile(path):
        os.remove(path)