from django import forms

from apps.users.models.user_models import Address
from utils.django_forms import add_placeholder


TAILWIND_INPUT_CLASS = 'w-full bg-black/50 border border-zinc-800 text-zinc-100 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-all placeholder-zinc-600'


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address', 'number', 'complement',
                  'neighborhood', 'cep', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = TAILWIND_INPUT_CLASS

        add_placeholder(self.fields['address'], 'Rua, avenida, etc.')
        add_placeholder(self.fields['number'], 'Número')
        add_placeholder(self.fields['complement'],
                        'Apartamento, bloco, referência...')
        add_placeholder(self.fields['neighborhood'], 'Bairro')
        add_placeholder(self.fields['cep'], '00000000')
        add_placeholder(self.fields['city'], 'Sua cidade')
