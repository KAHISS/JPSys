from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('verify-email/<uidb64>/<token>/',
         views.verify_email_view, name='verify_email'),
    path('resend-verification/', views.resend_verification_view,
         name='resend_verification'),
    path("", views.users_list, name="users_list"),
    path("detail/<int:pk>/", views.user_detail_view, name="user_detail"),
    path("detail/<int:user_pk>/address/create/",
         views.address_form_view, name="address_create"),
    path("detail/<int:user_pk>/address/edit/<int:pk>/",
         views.address_form_view, name="address_update"),
    path("create/", views.user_form_view, name="create_user"),
    path("edit/<int:pk>/", views.user_form_view, name="update_user"),
    path('edit/<int:pk>/reset-password/',
         views.admin_reset_password_view, name='reset_password'),
    path("delete/<int:pk>/", views.user_form_view, name="delete_user"),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path("search-clients/", views.get_clients_search, name="get_products_search"),
]
