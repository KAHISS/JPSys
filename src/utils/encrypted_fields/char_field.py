from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def get_fernet():
    return Fernet(settings.FIELD_ENCRYPTION_KEY.encode())


def calc_encrypted_max_length(max_length):
    """
    Calcula o tamanho máximo da coluna no banco considerando
    o overhead do Fernet (timestamp + IV + HMAC + base64).
    Aplica uma margem de segurança extra.
    """
    # Fórmula do Fernet: (n + 57) rounded up to multiple of 16, then base64 (~1.36x)
    estimated = int((max_length + 57) * 1.4)
    return estimated + 20  # margem de segurança extra


class EncryptedCharField(models.CharField):
    """
    CharField que criptografa o valor com Fernet antes de salvar
    e descriptografa automaticamente ao ler do banco.

    O max_length informado é validado sobre o valor ORIGINAL
    (antes de criptografar), não sobre o valor armazenado.
    """

    description = "CharField criptografado com Fernet"

    def __init__(self, *args, **kwargs):
        # Guarda o max_length "real" (do valor original) para validação
        self.original_max_length = kwargs.get('max_length', 255)

        # Sobrescreve o max_length que vai pro banco, calculando o espaço
        # necessário para caber o texto criptografado
        kwargs['max_length'] = calc_encrypted_max_length(
            self.original_max_length)

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        # Necessário para as migrations funcionarem corretamente
        name, path, args, kwargs = super().deconstruct()
        kwargs['max_length'] = self.original_max_length
        return name, path, args, kwargs

    def get_prep_value(self, value):
        if value is None or value == '':
            return value

        value = str(value)

        # Valida o tamanho ORIGINAL antes de criptografar
        if len(value) > self.original_max_length:
            raise ValidationError(
                f"Valor excede o tamanho máximo de {self.original_max_length} caracteres."
            )

        f = get_fernet()
        encrypted = f.encrypt(value.encode())
        return encrypted.decode()

    def from_db_value(self, value, expression, connection):
        if value is None or value == '':
            return value

        f = get_fernet()
        try:
            return f.decrypt(value.encode()).decode()
        except InvalidToken:
            # Dado corrompido, chave errada, ou valor legado não criptografado
            return value

    def to_python(self, value):
        return value

    def formfield(self, **kwargs):
        # Garante que o form use o max_length original, não o inflado
        defaults = {'max_length': self.original_max_length}
        defaults.update(kwargs)
        return super().formfield(**defaults)
