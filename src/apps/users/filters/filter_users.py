import django_filters
from django.db.models import Q
from django.contrib.auth import get_user_model

# Sempre use get_user_model() para referenciar seu model de usuário customizado
User = get_user_model()


class UserFilter(django_filters.FilterSet):
    # Campo de busca customizado que procura em vários campos de texto
    search = django_filters.CharFilter(
        method='custom_search',
        label='Buscar'
    )

    # Filtro exato para tipo de perfil
    type = django_filters.ChoiceFilter(
        choices=[('admin', 'Administrador'),
                 ('promoter', 'Promotora'), ('client', 'Client')],
        empty_label="Todos os Tipos"
    )

    class Meta:
        model = User
        fields = ['type']

    def custom_search(self, queryset, name, value):
        # O icontains faz a busca ignorando maiúsculas/minúsculas
        return queryset.filter(
            Q(username__icontains=value) |
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value) |
            Q(document__icontains=value)
        )
