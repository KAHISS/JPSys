const addItemsBtns = document.querySelectorAll('.add-to-cart');
const url = document.getElementById('action-url').value

console.log("uihidgffgfrhgf")

addItemsBtns.forEach(btn => {
    btn.addEventListener('click', function(event) {
        event.preventDefault();

        const div = event.currentTarget.parentNode
        const itemId = div.id;

        const csrfToken = div.querySelector('input[name="csrfmiddlewaretoken"]').value;

        if (itemId ) {
            const quantity = 1;
            updateCart(url, csrfToken, itemId, quantity);
        } else {
            alert('Dados do produto inválidos.');
        }
        
    });
});

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
            const toast = document.getElementById("cartCount")
            toast.innerText = data.cart_total_quantity
            alert("Produto adicionado ao carrinho com sucesso")
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