from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog_list, name='catalog_list'),
    path('perfil/', views.perfil, name='perfil'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.update_cart, name='update_cart'),
]
