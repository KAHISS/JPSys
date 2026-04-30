from django.db import models


class PromoterInventory(models.Model):
    class Meta:
        verbose_name = "inventário do promotor"
        verbose_name_plural = "inventários dos promotores"

    promoter = models.ForeignKey(
        'promoters.Promoter', on_delete=models.CASCADE, related_name='inventories', verbose_name="Promotor")
    inventory = models.ForeignKey(
        'inventory.Iventory', on_delete=models.CASCADE, related_name='promoter_inventories', verbose_name="Inventário")
    quantity = models.PositiveIntegerField("Quantidade", default=0)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return f"{self.promoter} - {self.inventory} (Quantidade: {self.quantity})"
