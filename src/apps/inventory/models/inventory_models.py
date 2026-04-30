from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    class meta:
        verbose_name = "inventario"
        verbose_name_plural = "inventarios"

    class Type(models.TextChoices):
        ACESSORY = "acessory", "Acessório"
        CHIP = "chip", "Chip"

    barcode = models.CharField(
        "Código de barras", max_length=255, unique=True, blank=True, null=True)
    type = models.CharField("Tipo", max_length=20, choices=Type.choices)
    description = models.CharField(
        "Descrição", max_length=355, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
    average_cost = models.DecimalField(
        "Custo médio", max_digits=10, decimal_places=2, blank=True, null=True)
    sale_price = models.DecimalField(
        "Preço de venda", max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(
        "Quantidade em estoque", default=0)
    image = models.ImageField(
        "Imagem", upload_to="inventory/covers/%Y/%m/%d/", blank=True, null=True)
    in_catalog = models.BooleanField("Em catálogo", default=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return f"{self.description or 'Sem descrição'}"
