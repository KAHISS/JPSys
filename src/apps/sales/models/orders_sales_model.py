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

    class PaymentMethod(models.TextChoices):
        PIX = "pix", "Pix"
        CREDIT_CARD = "credit_card", "Cartão de Crédito"
        DEBIT_CARD = "debit_card", "Cartão de Débito"
        CASH = "cash", "Dinheiro"

    client = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='orders_sales',
        verbose_name="Cliente"
    )
    status = models.CharField("Status", max_length=10,
                              choices=Status.choices, default='pending')
    payment_method = models.CharField(
        "Método de Pagamento",
        max_length=20,
        choices=PaymentMethod.choices,
        default='pix'
    )
    observations = models.TextField(
        blank=True, null=True, verbose_name="Observações")
    total_quantity = models.PositiveIntegerField(
        "Quantidade total de itens", default=1)
    total_value = models.DecimalField(
        "Value total", max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.client.get_full_name() or self.client.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        dados_itens = self.items.aggregate(
            total_qtd=models.Sum('quantity'),
            total_value=models.Sum(models.F('quantity')
                                   * models.F('unit_price'))
        )

        new_qtd = dados_itens.get('total_qtd') or 0
        new_value = dados_itens.get('total_value') or 0.00

        if self.total_quantity != new_qtd or self.total_value != new_value:
            self.total_quantity = new_qtd
            self.total_value = new_value
            super().save(update_fields=['total_quantity', 'total_value'])


class OrderItem(models.Model):
    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    order = models.ForeignKey(
        OrderSale, on_delete=models.CASCADE, related_name='items', verbose_name="Pedido")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="order_items", verbose_name="Produto")
    quantity = models.PositiveIntegerField("Quantidade", default=1)
    unit_price = models.DecimalField(
        "Preço Unitário", max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity}x {self.product.description} (Pedido #{self.order.id})"

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def save(self, *args, **kwargs):
        if self.pk is None:
            old_quantity = 0

        else:
            old_item = OrderItem.objects.get(pk=self.pk)
            old_quantity = old_item.quantity

        super().save(*args, **kwargs)

        if self.quantity != old_quantity:
            difference = self.quantity - old_quantity

            self.product.stock_quantity = models.F(
                'stock_quantity') - difference
            self.product.save()

        self.order.save()
