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
            'barcode': forms.TextInput(attrs={
                'class': 'w-full bg-[#121212] border border-[#333] text-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none',
                'placeholder': 'Ex: 1234567890123'
            }),
            'type': forms.Select(attrs={
                'class': 'w-full bg-[#121212] border border-[#333] text-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none appearance-none'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full bg-[#121212] border border-[#333] text-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none appearance-none'
            }),
            'description': forms.TextInput(attrs={
                'class': 'w-full bg-[#121212] border border-[#333] text-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none',
                'rows': 3,
                'placeholder': 'Ex: Capinha de celular resistente'
            }),
            'average_cost': forms.NumberInput(attrs={
                'class': 'w-full bg-[#121212] border border-[#333] text-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none',
                'placeholder': '0.00'
            }),
            'sale_price': forms.NumberInput(attrs={
                'class': 'w-full bg-[#121212] border border-[#333] text-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none',
                'placeholder': '0.00'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'w-full bg-[#121212] border border-[#333] text-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none',
                'placeholder': '0'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full text-gray-400 text-sm'
            }),
        }
