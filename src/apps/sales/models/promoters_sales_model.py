from django.db import models
from django.contrib.auth import get_user_model
from apps.inventory.models import PromoterStock

User = get_user_model()


class ChipSale(models.Model):
    class Meta:
        verbose_name = "venda de chip"
        verbose_name_plural = "vendas de chips"
        ordering = ['-created_at']

    promoter = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='chip_sales',
        verbose_name="Promotor",
        limit_choices_to={'type': 'promoter'}
    )

    product = models.ForeignKey(
        PromoterStock,
        on_delete=models.PROTECT,
        verbose_name="Chip (Produto)",
        limit_choices_to={'quantity__gt': 0}
    )

    iccid = models.CharField(
        "ICCID do Chip",
        max_length=25,
        unique=True,
        help_text="Número de série único impresso no chip físico"
    )

    service = models.BooleanField("Teve cadastro?", default=False)
    price_sold = models.DecimalField(
        "Valor do Chip na venda", max_digits=10, decimal_places=2)
    service_fee_sold = models.DecimalField(
        "Taxa de Serviço na venda", max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return f"Venda: {self.iccid} | Cliente: {self.customer_name} | Promotor: {self.promoter.first_name}"

    @property
    def total_value(self):
        if self.service:
            return self.price_sold + self.service_fee_sold
        return self.price_sold
