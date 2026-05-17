import django_filters
from django.db.models import Q
from apps.sales.models import ChipSale


class ChipSaleFilter(django_filters.FilterSet):
    # Busca customizada por ICCID, Nome do Cliente ou CPF
    search = django_filters.CharFilter(
        method='custom_search',
        label='Buscar (ICCID, Cliente ou CPF)'
    )

    service = django_filters.ChoiceFilter(
        label='Teve cadastro?',
        choices=[
            ('', 'Todos'),
            ('True', 'Sim'),
            ('False', 'Não')
        ],
        method='filter_service'
    )

    def filter_service(self, queryset, name, value):
        if value == 'True':
            return queryset.filter(service=True)
        elif value == 'False':
            return queryset.filter(service=False)
        return queryset

    # Filtro por período de data da venda (Muito útil para relatórios)
    start_date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='date__gte',
        label='A partir de'
    )
    end_date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='date__lte',
        label='Até'
    )

    class Meta:
        model = ChipSale
        fields = ['service']

    def custom_search(self, queryset, name, value):
        # Remove pontos e traços se o usuário digitar o CPF com máscara
        clean_value = value.replace('.', '').replace('-', '').strip()

        return queryset.filter(
            Q(iccid__icontains=value) |
            Q(customer_name__icontains=value) |
            Q(customer_cpf__icontains=clean_value)
        )
