from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('create/', views.product_form_view, name='create_product'),
    path('update/<int:pk>/', views.product_form_view, name='update_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('create/category/', views.category_view, name='create_category'),
    path('delete/category/', views.category_view, name='delete_category'),
    path("promoters/", views.promoter_inventory_list,
         name="promoter_inventory_list"),
    path("promoters/inventory/check", views.check_promoter_stock,
         name="promoter_inventory_check"),
    path('create/promoter/inventory', views.promotor_stock_view,
         name='create_promoter_inventory'),
    path("return/promoter/inventory", views.return_to_inventory_view,
         name="return_promoter_inventory"),
]
