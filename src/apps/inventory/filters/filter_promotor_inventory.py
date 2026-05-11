import django_filters
from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model
from apps.inventory.models import PromoterStock, Category

User = get_user_model()

# Variável de estilo do Tailwind para manter o padrão visual (usei azul para diferenciar do estoque principal)
TAILWIND_SELECT = 'w-full bg-black/50 border border-zinc-800 text-zinc-100 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all'

class PromoterStockFilter(django_filters.FilterSet):
    # Busca por texto (Código de barras ou Descrição do produto)
    search = django_filters.CharFilter(
        method='custom_search',
        label='Buscar Produto'
    )

    # Filtro por Promotor
    promoter = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(type='promoter', is_active=True),
        empty_label="Todos os Promotores",
        widget=forms.Select(attrs={'class': TAILWIND_SELECT})
    )

    # Filtro por Categoria (viaja até o model Product para achar a categoria)
    category = django_filters.ModelChoiceFilter(
        field_name='product__category',
        queryset=Category.objects.all(),
        empty_label="Todas as Categorias",
        widget=forms.Select(attrs={'class': TAILWIND_SELECT})
    )

    class Meta:
        model = PromoterStock
        fields = ['promoter', 'category']

    def custom_search(self, queryset, name, value):
        # O duplo underscore (__) permite buscar nos campos do Produto vinculado!
        return queryset.filter(
            Q(product__description__icontains=value) |
            Q(product__barcode__icontains=value)
        )