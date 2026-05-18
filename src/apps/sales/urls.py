from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('promoters/', views.promoters_sales_list, name='promoters_sales_list'),
    path('promoters/create/', views.promoter_sale_form_view, name='create_promoter_sale'),
    path("promoters/delete/<int:pk>/", views.delete_promoter_sale,
         name="delete_promoter_sale"),
    path('promoters/stock-price/', views.get_stock_price, name='get_stock_price'),
    path('orders/', views.teste, name="orders_sales_list")
]
