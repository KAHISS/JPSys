document.addEventListener('DOMContentLoaded', function() {
    // Pegamos os elementos da tela
    const productSelect = document.getElementById('id_product');
    const serviceCheckbox = document.getElementById('id_service');
    
    const displayPrice = document.getElementById('display-price');
    const displayFee = document.getElementById('display-fee');
    const displayTotal = document.getElementById('display-total');
    const clientDataSection = document.getElementById('client-data-section');

    // Variáveis para guardar os valores do chip selecionado atualmente
    let currentPrice = 0;
    let currentFee = 0;

    // 1. Função AJAX que vai no Django buscar os preços
    async function fetchPrices() {
        const stockId = productSelect.value;
        
        // Se o usuário voltou para a opção "Selecione...", zeramos tudo
        if (!stockId) {
            currentPrice = 0;
            currentFee = 0;
            updateScreen();
            return;
        }

        try {
            // Faz a requisição AJAX usando a url que criamos no passo 2
            const response = await fetch(`/sales/stock-price/?stock_id=${stockId}`);
            const data = await response.json();
            
            if (data.success) {
                currentPrice = data.price;
                currentFee = data.fee;
            } else {
                currentPrice = 0;
                currentFee = 0;
            }
            
            // Após buscar do servidor, manda atualizar a tela
            updateScreen();
            
        } catch (error) {
            console.error('Erro ao buscar preços do servidor:', error);
        }
    }

    // 2. Função que apenas calcula o total e faz a animação da tela
    function updateScreen() {
        // Mostra o preço do chip
        displayPrice.textContent = `R$ ${currentPrice.toFixed(2).replace('.', ',')}`;
        
        let total = currentPrice;

        // Se marcou que tem cadastro, cobra a taxa e mostra os campos do cliente
        if (serviceCheckbox.checked) {
            displayFee.textContent = `R$ ${currentFee.toFixed(2).replace('.', ',')}`;
            total += currentFee;
            
            // Mostra os dados do cliente
            clientDataSection.classList.remove('hidden');
            setTimeout(() => {
                clientDataSection.classList.add('opacity-100');
                clientDataSection.classList.remove('opacity-0');
            }, 10);
        } else {
            // Zera a taxa visualmente
            displayFee.textContent = `R$ 0,00`;
            
            // Esconde os dados do cliente
            clientDataSection.classList.add('opacity-0');
            clientDataSection.classList.remove('opacity-100');
            setTimeout(() => {
                clientDataSection.classList.add('hidden');
            }, 300);
        }

        // Mostra o Total Geral
        displayTotal.textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
    }

    // 3. Cadastra os eventos
    if (productSelect) {
        // Toda vez que mudar o produto, faz o AJAX
        productSelect.addEventListener('change', fetchPrices);
    }
    
    if (serviceCheckbox) {
        // Toda vez que clicar no checkbox, SÓ recalcula a tela (não precisa de AJAX de novo)
        serviceCheckbox.addEventListener('change', updateScreen);
    }

    // 4. Ao carregar a página (útil para edição), roda o AJAX inicial
    if (productSelect && productSelect.value) {
        fetchPrices();
    } else {
        updateScreen();
    }
});