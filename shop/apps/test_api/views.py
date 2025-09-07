from django.shortcuts import render

# Create your views here.

from apps.products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from .Serializers import ProductSerializer
from CustomPermissions import CustomPermissionForProductFeature

class AllProductsApi(APIView):
    permission_classes = [CustomPermissionForProductFeature]
    def get(self,request):
        products = Product.objects.filter(is_active = True).order_by('-published_date')
        self.check_object_permissions(request,products)
        ser_data = ProductSerializer(instance=products,many=True)
        return Response(data=ser_data.data)