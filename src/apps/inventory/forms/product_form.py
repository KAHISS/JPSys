from django import forms
from apps.inventory.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'barcode', 'type', 'category', 'description',
            'average_cost', 'sale_price', 'stock_quantity', 'image'
        ]
        widgets = {
            'barcode': forms.TextInput(attrs={'placeholder': 'Ex: 1234567890123'}),
            'description': forms.TextInput(attrs={'placeholder': 'Ex: Capinha de celular resistente'}),
            'average_cost': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'sale_price': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'stock_quantity': forms.NumberInput(attrs={'placeholder': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        default_class = 'w-full bg-black/50 border border-zinc-800 text-zinc-100 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-all placeholder-zinc-600'

        file_class = 'w-full text-zinc-400 text-sm file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-zinc-800 file:text-amber-500 hover:file:bg-zinc-700 transition-all cursor-pointer'

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = file_class
            else:
                field.widget.attrs['class'] = default_class
