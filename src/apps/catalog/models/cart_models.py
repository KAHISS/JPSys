from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal, ROUND_HALF_UP
from apps.sales.models import OrderSale, OrderItem
from apps.inventory.models import Product
from django.conf import settings
from django.db import transaction


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart', verbose_name="Usuário"
    )
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"

    def __str__(self):
        return f"Carrinho de {self.user.username}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.cart_items.all())

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.cart_items.all())

    @property
    def total_discount(self):
        """Soma de todos os descontos aplicados (ex: pacotes de atacado)"""
        return sum(item.discount for item in self.cart_items.all())

    def gerar_pedido(self, client=None, payment_method='pix', observations=""):

        if not self.cart_items.exists():
            raise ValueError("O carrinho está vazio.")

        cliente_final = client if client else self.user

        with transaction.atomic():

            # 1. Validação e Baixa de Estoque Seguro
            for item in self.cart_items.all():
                # Trava a linha do produto no banco para evitar concorrência
                produto_db = Product.objects.select_for_update().get(
                    id=item.product.id)

                if item.quantity > produto_db.stock_quantity:
                    raise ValueError(
                        f'Estoque insuficiente para "{produto_db.description}". Disponível: {produto_db.stock_quantity}')

                produto_db.stock_quantity -= item.quantity
                if produto_db.stock_quantity < 0:
                    produto_db.stock_quantity = 0
                produto_db.save()

            novo_pedido = OrderSale.objects.create(
                client=cliente_final,
                status=OrderSale.Status.PENDING,
                payment_method=payment_method,
                observations=observations,
                total_quantity=self.total_quantity,
                total_value=self.total_price
            )

            order_cart_items_batch = []
            for item in self.cart_items.all():
                preco_unit = item.product.sale_price if item.product.sale_price else Decimal(
                    '0.00')
                order_cart_items_batch.append(
                    OrderItem(
                        order=novo_pedido,
                        product=item.product,
                        quantity=item.quantity,
                        unit_price=preco_unit
                    )
                )

            OrderItem.objects.bulk_create(order_cart_items_batch)

            # 4. Limpa o carrinho
            self.cart_items.all().delete()

        return novo_pedido


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items', verbose_name="Carrinho"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Produto"
    )
    quantity = models.PositiveIntegerField("Quantidade", default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"

    def __str__(self):
        return f"{self.quantity}x {self.product.description} (Carrinho: {self.cart.user.username})"

    @property
    def subtotal(self):
        """Valor bruto (Qtd * Preço de Venda)"""
        if hasattr(self.product, 'sale_price') and self.product.sale_price:
            return self.product.sale_price * self.quantity
        return Decimal('0.00')

    def save(self, *args, **kwargs):
        if self.quantity < 1:
            self.delete()
        else:
            super().save(*args, **kwargs)
