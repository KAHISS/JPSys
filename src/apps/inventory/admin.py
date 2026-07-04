from django.contrib import admin
from .models import Category, Product, PromoterStock

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_per_page = 20

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "type", "category",
                    "stock_quantity", "average_cost", "sale_price",
                    "wholesale_price", "wholesale_min_quantity")
    search_fields = ("name", "category__name", "type", "barcode")
    list_filter = ("category", "type", "created_at", "updated_at")
    list_display_links = ("id", "description")
    list_per_page = 20

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


@admin.register(PromoterStock)
class PromoterStockAdmin(admin.ModelAdmin):
    list_display = ["id", "product"]

    class Meta:
        verbose_name = "Estoque da promotora"
        verbose_name_plural = "Estoques das Promotoras"


