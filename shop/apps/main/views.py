from django.shortcuts import render
from django.conf import settings
from django.views import View
from django.db.models import Q
from .models import Slider

def media_admin(request):
    return {"media_url":settings.MEDIA_URL}

def index(request):
    return render(request,"main_app/index.html")

# def test_view(request):
#     context={
#         'name':'masud',
#         'family':'ghasemi'
#     }
#     return render(request,'main_app/test.html',context)


def contactus(request):
    return render(request,'partials/main/contactus.html')





class SliderView(View):
    def get(self,request):
        # اسلایدر های فعال رو برام از دیتابیس بیار
        sliders = Slider.objects.filter(Q(is_active=True))
        return render(request,'main_app/sliders.html',{'sliders':sliders})
    
    
def handler404(request, exception=None):
    return render(request, 'main_app/404.html')