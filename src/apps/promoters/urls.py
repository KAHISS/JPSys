from django.urls import path
from . import views

app_name = 'promoters'

urlpatterns = [
    path('', views.chips_sales_list, name='chips')
]
