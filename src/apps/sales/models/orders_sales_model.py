from django.db import models
from django.contrib.auth import get_user_model
from apps.inventory.models import Product

User = get_user_model()

class OrderSale(models.Model):
    class Meta:
        verbose_name = "Pedido de Venda"
        verbose_name_plural = "Pedidos de Venda"
        ordering = ['-created_at']

    class Status(models.TextChoices):
        PENDING = "pending", "Pendente",
        PAID = "paid", "Pago",
        CANCELED = "canceled", "Cancelado"

    client = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='orders_sales',
        verbose_name="Cliente",
        limit_choices_to={'type__in': ['admin', 'promoter']}
    )
    status = models.CharField("Status", max_length=10, choices=Status.choices, default='pending')
    observations = models.TextField(blank=True, null=True, verbose_name="Observações")
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)


    def __str__(self):
        return f"Pedido #{self.id} - {self.client.get_full_name() or self.client.username}"
    
    @property
    def total_quantity(self):
        items = self.items.all()
        return sum(item.subtotal for item in items)
    
    @property
    def total_value(self):
        items = self.items.all()
        return sum(item.subtotal for item in items)


class OrderItem(models.Model):
    order = models.ForeignKey(OrderSale, on_delete=models.CASCADE, related_name='items', verbose_name="Pedido")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items", verbose_name="Produto")
    quantity = models.PositiveIntegerField("Quantidade", default=1)
    unit_price = models.DecimalField("Preço Unitário", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"{self.quantity}x {self.product.description} (Pedido #{self.order.id})"

    @property
    def subtotal(self):
        return self.quantity * self.unit_price