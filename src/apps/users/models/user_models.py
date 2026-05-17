from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    class Type(models.TextChoices):
        ADMIN = "admin", "Administrador"
        PROMOTER = "promoter", "Promotor"
        CLIENT = "client", "Cliente"

    type = models.CharField("Tipo", max_length=20, choices=Type.choices)
    phone = models.CharField("Telefone", max_length=11, blank=True, null=True)
    addres = models.CharField(
        "Endereço", max_length=255, blank=True, null=True)
    city = models.CharField(
        "Endereço", max_length=255, blank=True, null=True)
    document = models.CharField(
        "Documento", max_length=255, blank=True, null=True)
    comission = models.DecimalField(
        "Comissão", max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_type_display()})"
