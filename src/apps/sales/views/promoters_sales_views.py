from django.http import Http404, JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.pagination import make_pagination
from utils.reporting_metrics import get_promoters_sales_metrics
from apps.sales.forms import PromoterSaleForm
from apps.sales.models import ChipSale
from apps.inventory.models import PromoterStock
from apps.sales.filters import ChipSaleFilter

User = get_user_model()

PER_PAGE = 10


@login_required(login_url='users:login', redirect_field_name='next')
def promoters_sales_list(request):
    if not request.user.type in ["admin", "promoter"]:
        messages.error(
            request, f"Você está logado como {request.user.username}, mas precisa ser um administrador para acessar esta página.")
        return redirect('users:login')

    promoters_sales = User.objects.filter(
        type="promoter").order_by("-first_name")

    if request.user.is_superuser:
        queryset = ChipSale.objects.all().order_by('-created_at')
    if request.user.type == "promoter":
        queryset = ChipSale.objects.filter(
            promoter=request.user).order_by('-created_at')

    promoter_sale_filter = ChipSaleFilter(request.GET, queryset=queryset)

    sales, pagination_range = make_pagination(
        request, promoter_sale_filter.qs, PER_PAGE)

    metrics = get_promoters_sales_metrics(promoter_sale_filter.qs)

    get_copy = request.GET.copy()

    if 'page' in get_copy:
        del get_copy['page']

    additional_url_query = '&' + get_copy.urlencode() if get_copy else ''

    return render(request, 'sales/pages/promoters_sales.html', context={
        'page_title': 'Busca Avançada',
        'pagination_range': pagination_range,
        'objects': sales,
        'additional_url_query': additional_url_query,
        'promoters_sales_active': 'bg-amber-500 text-black font-semibold',
        'filter': promoter_sale_filter,
        "title": "Vendas de Chip",
        "page": "sales",
        'promoters_sales': promoters_sales,
        'total_sales_count': metrics['total_sales'] or 0,
        'total_revenue': metrics['revenue_sum'] or 0.00,
        'total_service_fee': metrics['service_fee_sum'] or 0.00,
        'total_services_count': metrics['services_count'] or 0,
        'total_commission': metrics['total_commission_sum'] or 0.00,
    })


@login_required(login_url='users:login', redirect_field_name='next')
def promoter_sale_form_view(request, pk=None):
    if not request.user.type in ["admin", "promoter"]:
        raise Http404("Você não tem acesso a essa página")

    products = PromoterStock.objects.filter(promoter=request.user)

    if pk:
        promoter_sale = get_object_or_404(ChipSale, id=pk)
        title = f"Editar Venda - {promoter_sale.id}#"
        path = f"Venda de chips > Editar Venda > {promoter_sale.id}"
        action = 'update'
        indentifier = promoter_sale.id
    else:
        promoter_sale = None
        title = "Registrar Venda"
        path = "Venda de chips > Registrar Venda"
        action = 'create'
        indentifier = None

    form = PromoterSaleForm(request.POST or None,
                            request.FILES or None, instance=promoter_sale)

    if request.method == 'POST':
        if form.is_valid():
            sale = form.save(commit=False)
            product = PromoterStock.objects.get(
                id=int(request.POST.get("id_product")))
            print(product)
            sale.product = product
            if not pk:
                if product.quantity <= 0:
                    messages.error(request, "Produto esgotado")
                    return redirect("sales:promoters_sales_list")
                product.quantity -= 1
                product.save()

            sale.promoter = request.user
            sale.price_sold = product.sale_price

            if sale.service:
                sale.service_fee_sold = sale.product.service_fee

            sale.save()

            messages.success(
                request, f"Venda {'atualizada' if pk else 'registrada'} com sucesso!")
            return redirect('sales:promoters_sales_list')
        else:
            messages.error(
                request, f"Erro ao {'atualizar' if pk else 'registrar'} venda. Verifique os dados e tente novamente.")

    return render(request, 'sales/pages/promoter_sale_form.html',
                  context={
                      "section": "sale",
                      "form": form,
                      "title": title,
                      "path": path,
                      "action": action,
                      'promoters_sales_active': 'bg-amber-500 text-black font-semibold',
                      "indentifier": indentifier,
                      "products": products,
                      "back_url": reverse('sales:promoters_sales_list'),
                      "page": "sale_form"
                  })


@login_required(login_url='users:login', redirect_field_name='next')
def delete_promoter_sale(request, pk):
    if not request.user.is_superuser or not request.POST:
        raise Http404("Você não tem permissão para deletar vendas")

    sale = ChipSale.objects.get(id=pk)

    sale.product.quantity += 1
    sale.product.save()

    messages.success(request, f"Venda {sale.id}# deletada com sucesso")

    sale.delete()

    return redirect("sales:promoters_sales_list")


@login_required(login_url='users:login', redirect_field_name='next')
def get_stock_price(request):
    stock_id = request.GET.get('stock_id')

    if stock_id:
        try:
            # Busca o estoque específico que o promotor selecionou
            stock = PromoterStock.objects.get(id=stock_id)
            return JsonResponse({
                'success': True,
                'price': float(stock.sale_price),
                'fee': float(stock.service_fee)
            })
        except PromoterStock.DoesNotExist:
            pass

    # Se der erro ou não achar, retorna zerado
    return JsonResponse({'success': False, 'price': 0.0, 'fee': 0.0})
