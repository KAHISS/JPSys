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
from apps.inventory.filters import ProductFilter
import json

User = get_user_model()

PER_PAGE = 10


@login_required(login_url='users:login', redirect_field_name='next')
def inventory_list(request):

    # 1. Verifica permissão
    if not request.user.is_superuser:
        messages.error(
            request, f"Você está logado como {request.user.username}, mas precisa ser um administrador para acessar esta página.")
        return redirect('users:login')

    promoters = User.objects.filter(
        type__in=["admin", "promoter"]).order_by("-first_name")
    queryset = Product.objects.all().order_by('-created_at')

    product_filter = ProductFilter(request.GET, queryset=queryset)

    products, pagination_range = make_pagination(
        request, product_filter.qs, PER_PAGE)
    
    metrics = get_inventory_metrics(product_filter.qs)

    get_copy = request.GET.copy()

    if 'page' in get_copy:
        del get_copy['page']

    additional_url_query = '&' + get_copy.urlencode() if get_copy else ''

    return render(request, 'inventory/pages/inventory.html', context={
        'page_title': 'Busca Avançada',
        'pagination_range': pagination_range,
        'objects': products,
        'additional_url_query': additional_url_query,
        'inventory_active': 'bg-amber-500 text-black font-semibold',
        'filter': product_filter,
        "title": "Estoque",
        "page": "inventory",
        'promoters': promoters,
        'total_products_count': metrics['total_products'] or 0,
        'total_units_in_stock': metrics['total_units'] or 0,
        'total_cost_value': metrics['total_cost'] or 0.00,
        'total_sales_potential': metrics['potential_revenue'] or 0.00,
        'profit_margin_percent': metrics['margin'] or 0.00,
        'total_profit': metrics['profit'],
    })


@login_required(login_url='users:login', redirect_field_name='next')
def product_form_view(request, pk=None):
    if not request.user.is_superuser:
        raise Http404("Você não tem permissão para acessar esta página.")

    if pk:
        product = get_object_or_404(Product, id=pk)
        title = f"Editar Produto - {product.description}"
        path = f"Estoque > Editar Produto > {product.description}"
        action = 'update'
        indentifier = product.id
    else:
        product = None
        title = "Registrar Produto"
        path = "Estoque > Registrar Produto"
        action = 'create'
        indentifier = None

    form = ProductForm(request.POST or None,
                       request.FILES or None, instance=product)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Produto {'atualizado' if pk else 'registrado'} com sucesso!")
            return redirect('inventory:inventory_list')
        else:
            messages.error(
                request, f"Erro ao {'atualizar' if pk else 'registrar'} produto. Verifique os dados e tente novamente.")

    return render(request, 'inventory/pages/product_form.html',
                  context={
                      "section": "stock",
                      "form": form,
                      "title": title,
                      "path": path,
                      "action": action,
                      "indentifier": indentifier,
                      "back_url": reverse('inventory:inventory_list'),
                      "page": "inventory"
                  })


@login_required(login_url='users:login', redirect_field_name='next')
def delete_product(request, pk):
    if not request.user.is_superuser and not request.POST:
        raise Http404("Você não tem permissão para acessar esta página.")

    product = get_object_or_404(Product, id=pk)

    if product.promoter_stock.exists():
        print(product.promoter_stock)
        messages.error(
            request, f"Produto '{product.description}' não pode ser excluido, pois existem distribuições vinculadas a ele")
        return redirect('inventory:inventory_list')

    product.delete()
    messages.success(
        request, f"Produto '{product.description}' excluído com sucesso!")
    return redirect('inventory:inventory_list')


@login_required(login_url='users:login', redirect_field_name='next')
def category_view(request):
    if not request.user.is_superuser and not request.POST:
        raise Http404("Você não tem permissão para acessar esta página.")

    try:
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create':
            nome = data.get('name')
            if nome:
                categoria = Category.objects.create(name=nome)
                return JsonResponse({'id': categoria.id, 'name': categoria.name}, status=201)
            return JsonResponse({'error': 'Nome inválido'}, status=400)

        elif action == 'delete':
            categoria_id = data.get('id')
            if categoria_id:
                categoria = get_object_or_404(Category, id=categoria_id)
                categoria.delete()
                return JsonResponse({'success': 'Categoria excluída com sucesso!'}, status=200)
            return JsonResponse({'error': 'ID da categoria não fornecido'}, status=400)

        else:
            return JsonResponse({'error': 'Ação inválida'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
