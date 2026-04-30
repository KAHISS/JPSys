from django.urls import path
from .views import login_view, login_create, logout_view

app_name = 'users'

urlpatterns = [
    # path('register/', views.register_view, name='register'),
    # path('register/create/', views.register_create, name='register_create'),
    path('login/', login_view, name='login'),
    path('login/create/', login_create, name='login_create'),
    path('logout/', logout_view, name='logout'),
]
