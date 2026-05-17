from django.contrib import admin
from .models import ChipSale

# Register your models here.


@admin.register(ChipSale)
class ChipSaleAdmin(admin.ModelAdmin):
    list_display = ("id",)
    search_fields = ("id",)
    list_per_page = 20

    class Meta:
        verbose_name = "Venda da promotora"
        verbose_name_plural = "Vendas das promotoras"
