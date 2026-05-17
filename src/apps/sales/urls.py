from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.promoters_sales_list, name='promoters_sales_list'),
    path('create/', views.promoter_sale_form_view, name='create_promoter_sale'),
    path("delete/<int:pk>/", views.delete_promoter_sale,
         name="delete_promoter_sale"),
    path('stock-price/', views.get_stock_price, name='get_stock_price'),
]
