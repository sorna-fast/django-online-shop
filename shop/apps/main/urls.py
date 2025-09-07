from django.urls import path
from .views import index,contactus,SliderView
app_name="main"
urlpatterns = [
    path("",index,name="index"),
    path("contactus",contactus,name="contactus"),
    # path("test/",test_view,name='test_view')
    path('sliders/',SliderView.as_view(),name="sliders"),
    # path('error/',handler404)
]
