from django.http import Http404, JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.pagination import make_pagination
from utils.reporting_metrics import get_orders_sales_metrics
from apps.sales.forms import OrderSaleForm
from apps.sales.models import OrderSale, OrderItem
from apps.inventory.models import PromoterStock, Product
from apps.sales.filters import OrderSaleFilter
from django.db import transaction
from django.db.models import Q

User = get_user_model()

PER_PAGE = 10


@login_required(login_url='users:login', redirect_field_name='next')
def orders_sales_list(request):
    orders_sales = User.objects.filter(
        type__in=["client", "promoter"]).order_by("-first_name")

    if request.user.is_superuser:
        queryset = OrderSale.objects.all().order_by('-created_at')
    else:
        queryset = OrderSale.objects.filter(
            client=request.user).order_by('-created_at')

    promoter_sale_filter = OrderSaleFilter(request.GET, queryset=queryset)

    sales, pagination_range = make_pagination(
        request, promoter_sale_filter.qs, PER_PAGE)

    metrics = get_orders_sales_metrics(promoter_sale_filter.qs)

    get_copy = request.GET.copy()

    if 'page' in get_copy:
        del get_copy['page']

    additional_url_query = '&' + get_copy.urlencode() if get_copy else ''

    return render(request, 'sales/pages/orders_sales.html', context={
        'page_title': 'Busca Avançada',
        'pagination_range': pagination_range,
        'objects': sales,
        'additional_url_query': additional_url_query,
        'orders_sales_active': 'bg-amber-500 text-black font-semibold',
        'filter': promoter_sale_filter,
        "title": "Meus Pedidos" if not request.user.is_superuser else "Pedidos de Venda",
        "page": "sales",
        'orders_sales': orders_sales,
        'total_orders_count': metrics['total_orders_count'],
        'total_revenue': metrics['total_revenue'] or 0.00,
        'total_pending': metrics['total_pending'] or 0.00,
        'total_canceled_count': metrics['total_canceled_count'],
    })


@login_required(login_url='users:login', redirect_field_name='next')
def cancel_order_sale(request, pk):
    # Trava de segurança: apenas admins
    if not request.user.is_superuser or not request.POST:
        messages.error(
            request, "Acesso negado. Apenas administradores podem cancelar pedidos.")
        return redirect('sales:orders_sales_list')

    order = get_object_or_404(OrderSale, id=pk)

    if order.status == OrderSale.Status.CANCELED:
        messages.warning(
            request, f"O Pedido #{order.id} já se encontra cancelado.")
    else:
        try:
            with transaction.atomic():

                order.status = OrderSale.Status.CANCELED
                order.save()

                for item in order.items.all():

                    estoque = item.product
                    estoque.stock_quantity += item.quantity
                    estoque.save()

            messages.success(
                request, f"Pedido #{order.id} cancelado e produtos devolvidos ao estoque com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao cancelar o pedido: {str(e)}")

    return redirect('sales:orders_sales_list')


@login_required(login_url='users:login')
def order_sale_detail_view(request, pk):
    order = get_object_or_404(OrderSale, id=pk)

    if request.method == 'POST':
        if not request.user.is_superuser or order.status == OrderSale.Status.CANCELED:
            messages.error(
                request, "Acesso negado ou pedido trancado para alterações.")
            return redirect('sales:order_resume', pk=order.id)

        form = OrderSaleForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            messages.success(
                request, f"Pedido #{order.id} atualizado com sucesso!")
            return redirect('sales:order_resume', pk=order.id)
        else:
            messages.error(
                request, "Erro ao atualizar o pedido. Verifique os dados informados.")

    else:
        if request.user.is_superuser and order.status != OrderSale.Status.CANCELED:
            form = OrderSaleForm(instance=order)
        else:
            form = None

    return render(request, 'sales/pages/order_resume.html', {
        'page_title': 'Resumo do pedido',
        'orders_sales_active': 'bg-amber-500 text-black font-semibold',
        "page": "sales_detail",
        'order': order,
        'form': form,
        'title': f"Detalhes do Pedido #{order.id}",
    })


@login_required(login_url='users:login', redirect_field_name='next')
def update_order_item(request, pk):
    if not request.user.is_superuser or not request.POST:
        raise Http404("Você não tem permissão para alterar os itens do pedido")

    item = OrderItem.objects.get(id=pk)
    order = request.POST.get("order")
    new_quantity = request.POST.get("quantity")

    try:
        item.quantity = int(new_quantity)
        messages.success(
            request, f"Quantidade do item '{item.product.description}' atualizada para {item.quantity}")
        item.save()
    except Exception as e:
        messages.error(request, f"Erro ao alterar quantidade do item {e}")

    return redirect("sales:order_resume", order)

@login_required(login_url='users:login', redirect_field_name='next')
def delete_order_item(request, pk):
    if not request.user.is_superuser or not request.POST:
        raise Http404("Você não tem permissão para alterar os itens do pedido")

    item = OrderItem.objects.get(id=pk)
    order = request.POST.get("order")

    try:
        item.product.stock_quantity += item.quantity
        item.product.save()
        item.delete()
        messages.success(
            request, f"Item '{item.product.description}' removido do pedido com sucesso!")
    except Exception as e:
        messages.error(request, f"Erro ao remover item do pedido {e}")

    return redirect("sales:order_resume", order)


@login_required(login_url='users:login', redirect_field_name='next')
def get_products_search(request):
    if not request.user.is_superuser or not request.GET:
        return JsonResponse({'results': []})

    query = request.GET.get('q', '')

    if not query:
        return JsonResponse({'results': []})

    products = Product.objects.filter(
        Q(description__icontains=query) | Q(barcode__icontains=query)
    )[:10]

    results = []
    
    for prod in products:
        results.append({
            'id': prod.id,
            'description': prod.description,
            'stock': prod.stock_quantity,
            'price': str(prod.sale_price),
        })

    return JsonResponse({'results': results})


@login_required(login_url='users:login', redirect_field_name='next')
def add_order_item(request, pk):
    if not request.user.is_superuser or not request.POST:
        raise Http404("Você não tem permissão para adicionar itens ao pedido")

    order = get_object_or_404(OrderSale, id=pk)

    product_id = request.POST.get("product_id")
    quantity = request.POST.get("quantity")

    try:
        product = Product.objects.get(id=product_id)

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=int(quantity),
            unit_price=product.sale_price
        )

        messages.success(
            request, f"Produto '{product.description}' adicionado ao pedido com sucesso!")
    except Exception as e:
        messages.error(request, f"Erro ao adicionar produto ao pedido {e}")

    return redirect("sales:order_resume", pk=order.id)