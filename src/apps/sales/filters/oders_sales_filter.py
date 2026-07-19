import django_filters
from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model
from apps.sales.models import OrderSale

User = get_user_model()

TAILWIND_SELECT = 'w-full bg-black/50 border border-zinc-800 text-zinc-100 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all'


class OrderSaleFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='custom_search',
        label='Buscar Pedido'
    )

    client = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(
            type__in=['admin', 'promoter'], is_active=True),
        empty_label="Todos os Clientes",
        widget=forms.Select(attrs={'class': TAILWIND_SELECT})
    )

    status = django_filters.ChoiceFilter(
        choices=OrderSale.Status.choices,
        empty_label="Todos os Status",
        widget=forms.Select(attrs={'class': TAILWIND_SELECT})
    )

    # --- FILTROS PARA DATA DE CRIAÇÃO ---
    # input_formats=['%Y-%m-%d'] força o Django a aceitar o padrão do input type="date"
    created_start = django_filters.DateFilter(
        field_name='created_at__date',
        lookup_expr='gte',
        input_formats=['%Y-%m-%d', '%d/%m/%Y']
    )
    created_end = django_filters.DateFilter(
        field_name='created_at__date',
        lookup_expr='lte',
        input_formats=['%Y-%m-%d', '%d/%m/%Y']
    )

    # --- FILTROS PARA DATA DE RETORNO ---
    return_start = django_filters.DateFilter(
        field_name='return_at',
        lookup_expr='gte',
        input_formats=['%Y-%m-%d', '%d/%m/%Y']
    )
    return_end = django_filters.DateFilter(
        field_name='return_at',
        lookup_expr='lte',
        input_formats=['%Y-%m-%d', '%d/%m/%Y']
    )

    class Meta:
        model = OrderSale
        fields = ['client', 'status']

    def custom_search(self, queryset, name, value):
        query = (
            Q(client__first_name__icontains=value) |
            Q(client__last_name__icontains=value) |
            Q(client__username__icontains=value) |
            Q(observations__icontains=value)
        )
        if value.strip().isdigit():
            query |= Q(id=value.strip())
        return queryset.filter(query)
