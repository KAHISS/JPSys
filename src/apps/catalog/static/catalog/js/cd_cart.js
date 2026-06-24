const cartForms = document.querySelectorAll('.add-quantity-form', '.remove-quantity-form');

// adiciona eventos nos botões de aumentar e diminuir quantidade
cartForms.forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        console.log("Form submitted:", this);
        const url = this.querySelector('input[name="url"]').value;
        const action = this.querySelector('input[name="action"]').value;
        const itemId = this.querySelector('input[name="item_id"]').value;
        console.log("itemId:", itemId, "action:", action);
        const csrfToken = this.querySelector('input[name="csrfmiddlewaretoken"]').value;

        if (itemId && action) {
            const quantity = action === 'increase' ? 1 : -1;
            updateCart(url, csrfToken, itemId, quantity, action);
        } else {
            alert('Dados do produto inválidos.');
        }
        
    });
});

// atualiza a quantidade do item no carrinho e os totais
const updateCartDisplay = (data) => {
    const itemElement = document.getElementById(`cart-item-${item.id}`);
    if (itemElement) {
        const quantitySpan = itemElement.getElementById('quantity');
        if (quantitySpan) {
            quantitySpan.innerText = data.cart_item.quantity;
        }
    }

    const totalQuantityElement = document.getElementById('total-quantity');
    const totalPriceElement = document.getElementById('total-price');
    if (totalQuantityElement) {
        totalQuantityElement.innerText = `Total (${data.cart_total_quantity} itens)`;
    }
    if (totalPriceElement) {
        totalPriceElement.innerText = `R$ ${data.cart_total_price.toFixed(2)}`;
    }
}

// atualiza o carrinho no backend e depois atualiza a exibição
const updateCart = (url, csrfToken, productId, quantity, action) => {

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            'product_id': productId,
            'quantity': quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartItem(data);
        } else {
            // Erro de estoque ou validação
            alert('Erro: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        alert('Erro ao tentar conectar com o servidor.');
    });
}

