from .models import Slider
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import os

@receiver(post_delete,sender=Slider)
def delete_slider_image_from_system_after_delete(request,**kwargs):
    path = settings.MEDIA_URL + str(kwargs['instance'].image_name)
    if os.path.isfile(path):
        os.remove(path)