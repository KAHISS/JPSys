from django.urls import path
from . import views

app_name = 'sale'

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('register/', views.register_product_view, name='register_product'),
]
