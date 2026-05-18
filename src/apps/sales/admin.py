from django.contrib import admin
from .models import ChipSale, OrderItem, OrderSale

# Register your models here.


@admin.register(ChipSale)
class ChipSaleAdmin(admin.ModelAdmin):
    list_display = ("id",)
    search_fields = ("id",)
    list_per_page = 20

    class Meta:
        verbose_name = "Venda da promotora"
        verbose_name_plural = "Vendas das promotoras"

@admin.register(OrderSale)
class OrderSaleAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "total_value", "total_quantity", "status", "created_at")
    search_fields = ("id", "client", "total_value", "total_quantity", "status", "created_at")
    list_display_links = ("id", "client", "total_value", "total_quantity", "status", "created_at")
    list_per_page = 20

    class Meta:
        verbose_name = "Pedido de venda"
        verbose_name_plural = "Pedidos de vendas"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "unit_price", "subtotal")
    search_fields = ("id", "product", "quantity", "unit_price", "subtotal")
    list_display_links = ("id", "product", "quantity", "unit_price", "subtotal")
    list_per_page = 20

    class Meta:
        verbose_name = "Item de pedido"
        verbose_name_plural = "Itens de pedidos"
