from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Address


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', "type", 'email',
                    'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'email', 'phone')
    ordering = ('id',)

    fieldsets = UserAdmin.fieldsets + (
        ('Informações Extras', {
         'fields': ('type', 'phone', 'document')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Extras', {
         'fields': ('type', 'phone', 'document')}),
    )

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'number',
                    'neighborhood', 'complement', 'city', 'cep')
    list_filter = ('city', 'neighborhood')
    list_display_links = ('id', 'user')
    search_fields = ('user__username', 'address', 'number',
                     'neighborhood', 'complement', 'city', 'cep')
    ordering = ('id',)

    fieldsets = (
        ('Informações do endereço', {
            'fields': ('user', 'address', 'number', 'complement', 'neighborhood', 'cep', 'city')
        }),
    )

    class Meta:
        verbose_name = "endereço"
        verbose_name_plural = "endereços"
