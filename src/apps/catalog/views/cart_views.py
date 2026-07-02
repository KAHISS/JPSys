from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib import messages
import json
from django.http import JsonResponse
from apps.catalog.models import Cart, CartItem
from apps.sales.models import OrderSale, OrderItem
from apps.inventory.models import Product

User = get_user_model()


@login_required(login_url='users:login')
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'catalog/pages/cart.html', context={
        'cart': cart,
        'page_title': 'Meu Carrinho',
        "title": "Carrinho",
        "page": "cart",
    })


@login_required(login_url='users:login')
def update_cart(request):
    if request.method != "POST":
        return JsonResponse({'success': False, 'message': 'Acesso inválido. Esperado POST.'}, status=400)
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        product_id = data.get('product_id')

        try:
            quantity = int(data.get('quantity'))

        except ValueError:
            return JsonResponse({'success': False, 'message': 'Quantidade inválida.'}, status=400)

        print("ola efewfwe")
        product = get_object_or_404(Product, id=product_id)

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )

        if item_created:
            nova_quantidade = 1
        else:
            nova_quantidade = cart_item.quantity + quantity

        if product.stock_quantity and nova_quantidade > product.stock_quantity:
            return JsonResponse({
                'success': False,
                'message': f'Estoque insuficiente. Restam apenas {product.stock_quantity} unidades.'
            }, status=400)

        cart_item.quantity = nova_quantidade
        cart_item_id = cart_item.id

        if cart_item.quantity <= 0:
            deleted = True

            cart_item.delete()
        else:
            deleted = False
            cart_item.save()

        return JsonResponse({
            'success': True,
            'deleted': deleted,
            'message': f'{quantity}x {product.description} adicionado ao carrinho!',
            'cart_total_quantity': cart.total_quantity,
            'cart_total_price': f'{cart.total_price:,.2f}',
            'cart_item': {
                'id': cart_item_id,
                'quantity': cart_item.quantity,
                'total_price': f'R$ {cart_item.subtotal:,.2f}'
            }
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)


@login_required(login_url='users:login')
def deleteCartItem(request, pk):
    if request.method != "POST":
        messages.error(request, "Requisição invalida")
        redirect('catalog:cart')

    cart_item = CartItem.objects.get(id=pk)

    cart_item.delete()

    messages.success(request, "Item deletado com sucesso")

    return redirect("catalog:cart")


@login_required(login_url='users:login')
def checkout_cart(request):
    if request.method != 'POST':
        messages.error(request, "Acesso inválido.")
        return redirect('catalog:cart')

    cart = get_object_or_404(Cart, user=request.user)

    # 1. Captura as escolhas do usuário no formulário HTML
    payment_method = request.POST.get(
        'payment_method', OrderSale.PaymentMethod.PIX)
    observations = request.POST.get('observations', '')

    # Se for Admin, verifica se ele escolheu outro cliente para a venda
    cliente_venda = request.user
    if request.user.is_superuser or request.user.is_staff:
        client_id = request.POST.get('client_id')
        if client_id:
            cliente_venda = User.objects.get(id=client_id)

    # 2. Tenta gerar o pedido usando a inteligência do nosso Model!
    try:
        novo_pedido = cart.gerar_pedido(
            client=cliente_venda,
            payment_method=payment_method,
            observations=observations
        )

        messages.success(
            request, f'Pedido #{novo_pedido.id} gerado com sucesso!')
        return redirect('sales:order_resume', pk=novo_pedido.id)

    except ValueError as e:
        # Cai aqui se o carrinho estiver vazio ou se der erro de estoque insuficiente
        messages.error(request, str(e))
        return redirect('catalog:cart')

    except Exception as e:
        messages.error(
            request, f"Erro inesperado ao processar a compra: {str(e)}")
        return redirect('catalog:cart')
