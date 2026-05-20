from django import forms
from apps.sales.models import OrderSale


class OrderSaleForm(forms.ModelForm):
    class Meta:
        model = OrderSale
        fields = [
            'client', 'status', 'observations', 'payment_method'
        ]
        widgets = {
            'observations': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Adicione observações ou detalhes sobre o andamento do pedido...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Padrão para inputs, selects e textareas (com focus em emerald/verde)
        default_class = 'w-full bg-black/50 border border-zinc-800 text-zinc-100 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all placeholder-zinc-600'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = default_class
