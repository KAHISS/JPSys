from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog_list, name='catalog_list'),
    path('perfil/', views.perfil, name='perfil'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:pk>', views.deleteCartItem, name='delete_cart_item'),
    path('cart/checkout/', views.checkout_cart, name='checkout')
]
