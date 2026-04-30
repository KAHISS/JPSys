from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', "type", 'email',
                    'addres', 'city', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'email', 'addres', 'city', 'phone')
    ordering = ('id',)

    fieldsets = UserAdmin.fieldsets + (
        ('Informações Extras', {
         'fields': ('type', 'addres', 'city', 'phone', 'document')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Extras', {
         'fields': ('type', 'addres', 'city', 'phone', 'document')}),
    )

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"
