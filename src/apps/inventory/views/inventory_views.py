from datetime import timedelta
from django.utils import timezone
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.settings import STATIC_URL
from django.middleware.csrf import get_token
from utils.pagination import make_pagination
from apps.inventory.forms import ProductForm
from apps.inventory.models import Product, Category
from django.db.models import Q, Sum
from decimal import Decimal
import json
import os


PER_PAGE = 10


@login_required(login_url='users:login', redirect_field_name='next')
def sale_list(request):
    # 1. Verifica permissão
    if not request.user.is_superuser:
        messages.error(
            request, f"Você está logado como {request.user.username}, mas precisa ser um administrador para acessar esta página.")
        return redirect('users:login')

    products = Product.objects.all().order_by('-created_at')

    # 3. Aplica o Filtro (Isso é o mais importante)
    # = SaleFilter(request.GET, queryset=sales_qs)

    # Daqui para baixo, usamos 'sale_filter.qs' (que são os dados filtrados)
    # e não mais 'sales_qs' (que são todos os dados)

    # 4. Estatísticas (Agora baseadas no filtro)
    stats = {
        'total_products': products.count(),
        'total_cost': products.aggregate(Sum('average_cost'))['average_cost__sum'] or 0,

        # Aqui mantivemos a lógica de status, mas dentro do universo filtrado
        'total_orders_pending': products.filter(status='pendente').count(),
        'total_sales_pending': products.filter(status='pendente').aggregate(Sum('total_price'))['total_price__sum'] or 0,

        'total_orders_completed': products.filter(status='pago').count(),
        'total_sales_completed': products.filter(status='pago').aggregate(Sum('total_price'))['total_price__sum'] or 0,

        'total_orders_cancelled': products.filter(status='cancelado').count(),
        'total_sales_cancelled': products.filter(status='cancelado').aggregate(Sum('total_price'))['total_price__sum'] or 0,
    }

    # 5. Paginação
    page_obj, pagination_range = make_pagination(
        request, filtered_qs, PER_PAGE)

    # 6. Preservar filtros na paginação
    # Copia os parâmetros GET da URL (ex: ?seller=joao&status=pago)
    get_copy = request.GET.copy()
    # Remove o parâmetro 'page' atual para não duplicar (ex: page=1&page=2)
    if 'page' in get_copy:
        del get_copy['page']
    # Transforma em string para usar no template (ex: "&seller=joao&status=pago")
    additional_url_query = '&' + get_copy.urlencode() if get_copy else ''

    return render(request, 'sale/pages/pdv.html', context={
        'page_title': 'Busca Avançada',
        'sales': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': additional_url_query,
        'stats': stats,
        'filter': sale_filter,  # AQUI está a correção do erro original
    })


@login_required(login_url='users:login', redirect_field_name='next')
def inventory_list(request):
    if not request.user.is_superuser:
        raise Http404("Você não tem permissão para acessar esta página.")
    return render(request, 'inventory/pages/inventory.html',
                  context={
                      "section": "stock",
                      "title": "Estoque",
                      "path": "Estoque",
                      "back_url": reverse('inventory:inventory_list'),
                  })


@login_required(login_url='users:login', redirect_field_name='next')
def register_product_view(request):
    if not request.user.is_superuser:
        raise Http404("Você não tem permissão para acessar esta página.")

    form = ProductForm()
    return render(request, 'inventory/pages/register_product.html',
                  context={
                      "section": "stock",
                      "form": form,
                      "title": "Registrar Produto",
                      "path": "Estoque > Registrar Produto",
                      "back_url": reverse('inventory:inventory_list'),
                  })
