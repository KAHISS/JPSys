from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.pagination import make_pagination
from utils.reporting_metrics import get_promoters_inventory_metrics
from apps.inventory.models import PromoterStock, Product
from django.http import Http404, JsonResponse
from apps.inventory.filters import PromoterStockFilter
from django.shortcuts import render

User = get_user_model()

PER_PAGE = 10


@login_required(login_url='users:login', redirect_field_name='next')
def promoter_inventory_list(request):
    # 1. Verifica permissão
    if not request.user.type in ["admin", "promoter"]:
        messages.error(
            request, f"Você está logado como {request.user.username}, mas precisa ser um administrador ou promotor para acessar esta página.")
        return redirect('users:login')

    if request.user.is_superuser:
        queryset = PromoterStock.objects.all().order_by('-created_at')
    if request.user.type == "promoter":
        queryset = PromoterStock.objects.filter(
            promoter=request.user).order_by('-created_at')

    product_filter = PromoterStockFilter(request.GET, queryset=queryset)

    products, pagination_range = make_pagination(
        request, product_filter.qs, PER_PAGE)

    metrics = get_promoters_inventory_metrics(product_filter.qs)

    get_copy = request.GET.copy()

    if 'page' in get_copy:
        del get_copy['page']

    additional_url_query = '&' + get_copy.urlencode() if get_copy else ''

    return render(request, 'inventory/pages/promoter_inventory.html', context={
        'page_title': 'Busca Avançada',
        'pagination_range': pagination_range,
        'objects': products,
        'additional_url_query': additional_url_query,
        'promoter_inventory_active': 'bg-amber-500 text-black font-semibold',
        'filter': product_filter,
        "title": "Estoque de promotores",
        "page": "inventory",
        'total_promoters_with_stock': metrics['unique_promoters'] or 0,
        'total_chips_in_hand': metrics['total_units'] or 0,
        'total_potential_revenue': metrics['potential_revenue'] or 0.00,
        'total_potential_revenue_with_service': metrics['potential_revenue_with_service'] or 0,
    })


@login_required(login_url='users:login', redirect_field_name='next')
def promotor_stock_view(request):
    if not request.user.is_superuser and not request.POST:
        raise Http404("Você não tem permissão para acessar esta página.")
    # Pega os dados direto do request.POST
    product_id = request.POST.get('product_id')
    promoter_id = (request.POST.get('promoter_id'))
    quantity = int(request.POST.get('quantity', 0))
    sale_price = request.POST.get('sale_price', 0)
    service_fee = request.POST.get('service_fee', 0)
    type_user = request.POST.get('type', "promoter")

    if quantity <= 0:
        messages.error(request, 'A quantidade deve ser maior que zero.')
        # Altere para o nome da sua url de lista
        return redirect('inventory:inventory_list')
    print(promoter_id)

    try:
        with transaction.atomic():
            product = get_object_or_404(Product, id=product_id)
            promoter = get_object_or_404(
                User, id=promoter_id)

            if product.stock_quantity < quantity:
                messages.error(
                    request, 'Estoque insuficiente no inventário central.')
                return redirect('inventory:inventory_list')

            # 1. Desconta do inventário principal
            product.stock_quantity -= quantity
            product.save()

            # 2. Adiciona ao estoque do promotor
            promoter_stock, created = PromoterStock.objects.get_or_create(
                promoter=promoter,
                product=product,
                defaults={
                    'quantity': 0,
                    'sale_price': sale_price or 0.00,
                    'service_fee': service_fee or 0.00
                }
            )

            promoter_stock.quantity += quantity
            if sale_price:
                promoter_stock.sale_price = sale_price
            if service_fee:
                promoter_stock.service_fee = service_fee
            promoter_stock.save()

        # Usando o sistema de mensagens do Django!
        messages.success(
            request, f'{quantity}x {product.description} transferidos para {promoter.first_name}!')

    except Exception as e:
        messages.error(request, f'Erro ao transferir estoque: {str(e)}')

    # No final, redireciona de volta para a lista (recarrega a página automaticamente)
    return redirect('inventory:inventory_list')


@login_required(login_url='users:login', redirect_field_name='next')
def check_promoter_stock(request):
    product_id = request.GET.get('product_id')
    promoter_id = request.GET.get('promoter_id')

    if product_id and promoter_id:
        # Retorna True se o registro existir, False se não existir
        product = PromoterStock.objects.filter(
            product_id=product_id, promoter_id=promoter_id)
        
        if product:
            return JsonResponse({'exists': True, 'sale_price': product[0].sale_price, 'service_fee': product[0].service_fee})
        else:
            product = Product.objects.get(id=product_id)
            return JsonResponse({'exists': False, 'sale_price': product.sale_price})

    return JsonResponse({'exists': False})


@login_required(login_url='users:login', redirect_field_name='next')
@transaction.atomic
def return_to_inventory_view(request):
    if not request.user.is_superuser and not request.POST:
        raise Http404("Você não tem permissão para acessar esta página.")

    stock_id = request.POST.get('stock_id')
    print(stock_id)
    qty_to_return = int(request.POST.get('quantity', 0))

    promoter_stock = get_object_or_404(PromoterStock, id=stock_id)
    product = promoter_stock.product

    if qty_to_return > promoter_stock.quantity:
        messages.error(request, "Quantidade inválida para retorno.")
        return redirect('inventory:promoter_stock_list')

    promoter_stock.quantity -= qty_to_return

    product.stock_quantity += qty_to_return
    product.save()

    promoter_stock.save()

    messages.success(
        request, f"Sucesso! {qty_to_return} unidades de {product.description} retornaram ao Estoque Central.")

    return redirect('inventory:promoter_inventory_list')
