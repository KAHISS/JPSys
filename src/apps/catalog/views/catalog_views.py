from django.http import Http404, JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.pagination import make_pagination
from utils.reporting_metrics import get_inventory_metrics
from apps.inventory.forms import ProductForm
from apps.inventory.models import Product, Category
from apps.catalog.models import Cart
from apps.inventory.filters import ProductFilter
from django.db.models import Q
import json

User = get_user_model()

PER_PAGE = 15


def catalog_list(request):

    search_term = request.GET.get('q', '').strip()
    category_id = request.GET.get('category_id', '').strip()

    additional_url_query = f'&q={search_term}' if search_term else ''

    if category_id:
        queryset = Product.objects.filter(
            stock_quantity__gt=0,
            category__id=int(category_id)
        ).filter(
            Q(description__icontains=search_term) |
            Q(barcode__icontains=search_term)
        ).distinct().order_by("category__name")

        additional_url_query += f'&category_id={category_id}'
    else:
        queryset = Product.objects.filter(
            stock_quantity__gt=0
        ) .filter(
            Q(description__icontains=search_term) |
            Q(barcode__icontains=search_term)
        ).distinct().order_by("category__name")

    categories = Category.objects.all().order_by("name")

    cart = Cart.objects.get(
        user=request.user) if request.user.is_authenticated else None

    products, pagination_range = make_pagination(
        request, queryset, PER_PAGE)

    print(queryset)

    return render(request, 'catalog/pages/catalog.html', context={
        'page_title': 'Busca Avançada',
        'pagination_range': pagination_range,
        'objects': products,
        'additional_url_query': additional_url_query,
        "title": "Catalogo",
        "page": "catalog",
        'categories': categories,
        'cart': cart,
    })


@login_required(login_url='users:login', redirect_field_name='next')
def perfil(request):
    return render(request, 'catalog/pages/perfil.html', context={
        "title": "Perfil",
        "page": "perfil",
    })
