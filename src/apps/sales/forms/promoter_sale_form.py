from django import forms
from apps.sales.models import ChipSale


class PromoterSaleForm(forms.ModelForm):
    class Meta:
        model = ChipSale
        fields = [
            'iccid', 'service',
            'customer_name', 'customer_cpf', 'customer_birth_date'
        ]
        widgets = {
            'iccid': forms.TextInput(attrs={'placeholder': 'Bipe ou digite o código do chip'}),
            'customer_name': forms.TextInput(attrs={'placeholder': 'Ex: João da Silva'}),
            'customer_cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00', 'maxlength': '14'}),
            'customer_birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Padrão para inputs de texto, números, selects e datas (com focus em emerald/verde)
        default_class = 'w-full bg-black/50 border border-zinc-800 text-zinc-100 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all placeholder-zinc-600'

        # Padrão específico para o Checkbox (campo 'service')
        checkbox_class = 'w-5 h-5 rounded border-zinc-800 bg-black/50 text-emerald-500 focus:ring-emerald-500 focus:ring-offset-zinc-900 transition-all cursor-pointer'

        for field_name, field in self.fields.items():
            # Aplica o estilo de checkbox se for campo booleano
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = checkbox_class
            else:
                field.widget.attrs['class'] = default_class
