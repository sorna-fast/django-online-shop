from django.urls import path
from . import views

app_name = 'test_api'

urlpatterns = [
    path('products/',views.AllProductsApi.as_view(),name="products"),
]