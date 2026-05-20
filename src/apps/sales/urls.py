from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('promoters/', views.promoters_sales_list, name='promoters_sales_list'),
    path('promoters/create/', views.promoter_sale_form_view,
         name='create_promoter_sale'),
    path("promoters/delete/<int:pk>/", views.delete_promoter_sale,
         name="delete_promoter_sale"),
    path('promoters/stock-price/', views.get_stock_price, name='get_stock_price'),
    path('orders/', views.orders_sales_list, name="orders_sales_list"),
    path("orders/cancel/<int:pk>", views.cancel_order_sale, name="cancel_order"),
    path("orders/resume/<int:pk>",
         views.order_sale_detail_view, name="order_resume"),
    path("orders/edit/<int:pk>", views.update_order_item, name="update_order_item")
]
