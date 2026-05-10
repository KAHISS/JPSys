import django_filters
from django.db.models import Q
from apps.inventory.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    # Campo de busca customizado que procura tanto no código de barras quanto na descrição
    search = django_filters.CharFilter(
        method='custom_search',
        label='Buscar'
    )

    # Filtro exato para tipo
    type = django_filters.ChoiceFilter(
        choices=Product.Type.choices,
        empty_label="Todos os Tipos"
    )

    # Filtro por categoria
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        empty_label="Todas as Categorias"
    )

    class Meta:
        model = Product
        fields = ['type', 'category']

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(description__icontains=value) |
            Q(barcode__icontains=value)
        )
