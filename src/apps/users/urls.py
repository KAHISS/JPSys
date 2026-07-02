from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # path('register/', views.register_view, name='register'),
    # path('register/create/', views.register_create, name='register_create'),
    path("", views.users_list, name="users_list"),
    path("create/", views.user_form_view, name="create_user"),
    path("edit/<int:pk>/", views.user_form_view, name="update_user"),
    path('edit/<int:pk>/reset-password/',
         views.admin_reset_password_view, name='reset_password'),
    path("delete/<int:pk>/", views.user_form_view, name="delete_user"),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path("search-clients/", views.get_clients_search, name="get_products_search"),
]
