const updateBtns = document.querySelectorAll('.update-btn');
const url = document.getElementById('action-url').value

// adiciona eventos nos botões de aumentar e diminuir quantidade e de adicionar items no carrinho
updateBtns.forEach(btn => {
    btn.addEventListener('click', function(event) {
        event.preventDefault();

        const action = event.currentTarget.value;
        const form = event.currentTarget.parentNode
        const itemId = form.id;
        const span = parseInt(form.querySelector('#quantity').innerText)
   
        if (span - 1 <= 0 && action === "decrease") {
            return
        }

        const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

        if (itemId && action) {
            const quantity = action === 'increase' ? 1 : -1;
            updateCart(url, csrfToken, itemId, quantity);
        } else {
            alert('Dados do produto inválidos.');
        }
        
    });
});

// atualiza a quantidade do item no carrinho e os totais
const updateCartDisplay = (data) => {
    const itemElement = document.getElementById(`cart-item-${data.cart_item.id}`);

    if (data.deleted) {
        itemElement.remove()
        return
    }

    if (itemElement) {
        const quantitySpan = itemElement.querySelector('#quantity');
        const subtotal = itemElement.querySelector('#subtotal');
        if (quantitySpan && subtotal) {
            quantitySpan.innerText = data.cart_item.quantity;
            subtotal.innerText = `${data.cart_item.total_price}`.replace(".", ",");
        }
    }

    const totalQuantityElement = document.getElementById('total-quantity');
    const totalPriceElement = document.getElementById('total-price');
    if (totalQuantityElement) {
        totalQuantityElement.innerText = `Total (${data.cart_total_quantity} itens)`;
    }
    if (totalPriceElement) {
        totalPriceElement.innerText = `R$ ${data.cart_total_price}`;
    }
}

// atualiza o carrinho no backend e depois atualiza a exibição
const updateCart = (url, csrfToken, productId, quantity) => {

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
            updateCartDisplay(data);
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

