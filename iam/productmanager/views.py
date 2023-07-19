from django.shortcuts import render
import requests
from rest_framework import viewsets
from .serializers import DeviceSerializer
from .models import Device


def product_manager(request):
    products = "Loan management system"
    image_test = "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg"
    product_desc = "Easy to manage your customer and investment return tracking"
    
        
    return render(request, 'products/products.html', {'products': products, 'image_test': image_test, 'product_desc': product_desc})


class DeviceViewSet(viewsets.ModelViewSet):
    
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
