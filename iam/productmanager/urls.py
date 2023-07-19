from django.urls import path
from . import views


# URL of Product Manager
urlpatterns = [
    path('manager/product/', views.product_manager, name="products_manager"), 
]
