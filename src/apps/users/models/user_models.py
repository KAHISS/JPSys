from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.encrypted_fields import EncryptedCharField


class User(AbstractUser):
    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    class Type(models.TextChoices):
        ADMIN = "admin", "Administrador"
        PROMOTER = "promoter", "Promotor"
        CLIENT = "client", "Cliente"

    type = models.CharField("Tipo", max_length=20, choices=Type.choices)
    phone = EncryptedCharField(
        "Telefone", max_length=11, blank=True, null=True)
    document = EncryptedCharField(
        "Documento", max_length=15, blank=True, null=True)
    comission = models.DecimalField(
        "Comissão", max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_type_display()})"


class Address(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="address",
        verbose_name="Usuário",
    )

    address = EncryptedCharField(
        "Endereço", max_length=255, blank=True, null=True)
    number = EncryptedCharField("Número", max_length=20, blank=True, null=True)
    neighborhood = models.CharField(
        "Bairro", max_length=255, blank=True, null=True)
    complement = EncryptedCharField(
        "Complemento", max_length=255, blank=True, null=True)
    cep = models.CharField("CEP", max_length=8, blank=True, null=True)
    city = models.CharField("Cidade", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "endereço"
        verbose_name_plural = "endereços"

    def __str__(self):
        return f"{self.address} - {self.city}"
