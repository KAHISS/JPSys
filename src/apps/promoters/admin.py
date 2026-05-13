from django.contrib import admin
from apps.promoters.models import ChipSale

# Register your models here.


@admin.register(ChipSale)
class ChipSaleAdmin(admin.ModelAdmin):
    list_display = ("promoter", "product")
    search_fields = ("promoter", "product")

    class Meta:
        verbose_name = "Venda de chip"
        verbose_name_plural = "Vendas de chips"
