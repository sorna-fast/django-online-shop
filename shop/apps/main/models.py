from django.db import models
from utils import FileUpload
from django.utils import timezone
from django.utils.html import mark_safe
# ممکنه روی اسلایدر چند تا متن قرار بده که واسه این منظور 3 تا اسلایدر تایتل قرار دادم
# slider_link : قابل کلیک شدن اسلایدر
class Slider(models.Model):
    slider_title1 = models.CharField(max_length=500,null=True,blank=True,verbose_name="متن اول")
    slider_title2 = models.CharField(max_length=500,null=True,blank=True,verbose_name="متن دوم")
    slider_title3 = models.CharField(max_length=500,null=True,blank=True,verbose_name="متن سوم")
    
    file_upload = FileUpload('images','slides')
    image_name = models.ImageField(upload_to=file_upload.upload_to,verbose_name="تصویر اسلایدر")
    
    slider_link = models.URLField(max_length=200,null=True,blank=True,verbose_name="لینک")
    
    is_active = models.BooleanField(default=True,blank=True,verbose_name="وضعیت فعال/غیرفعال")
    
    register_date = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ درج")
    publish_date = models.DateTimeField(default=timezone.now,verbose_name="تاریخ انتشار")
    update_date = models.DateTimeField(auto_now=True,verbose_name="تاریخ اخرین بروزرسانی")
    
    def __str__(self):
        return f"{self.slider_title1}"
    
    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدر ها"
        
    # نوشتن کدی برای نمایش عکس در پنل مدیریت
    # mark_safe : یک کد اچ تی ام ال رو به صورت رشته دریافت میکنه و اونو اجرا میکنه
    def image_slide(self):
        return mark_safe(f'<img src="/media/{self.image_name}" style="width:80px; height:80px"/>')
    
    image_slide.short_description = "تصویر اسلاید"
    
    
    # میخوام لینک اسلایدر از توی پنل ادمین هم قابل کلیک کردن باشه
    def link(self):
        return mark_safe(f'<a href="{self.slider_link} target="_blank">link</a>')
    
    link.short_description = 'پیوندها'