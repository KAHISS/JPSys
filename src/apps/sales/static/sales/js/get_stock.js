// Variável para evitar mandar dezenas de requisições se o usuário digitar muito rápido (Debounce)
let searchTimeout = null;

function searchProducts(query) {
    const resultsList = document.getElementById('product-search-results');
    const addBtn = document.getElementById('add-product-btn');
    
    // Se apagar o texto, esconde a lista e bloqueia o botão
    if (query.trim().length < 2) {
        resultsList.classList.add('hidden');
        resultsList.innerHTML = '';
        document.getElementById('selected-product-id').value = '';
        disableAddButton(addBtn);
        return;
    }

    clearTimeout(searchTimeout);
    
    // Espera 300ms após o usuário parar de digitar para fazer a busca
    searchTimeout = setTimeout(() => {
        // AQUI: Você precisa criar uma view no Django que retorne um JSON com base nessa URL
        fetch(`/sales/orders/items/search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                resultsList.innerHTML = ''; // Limpa a lista
                
                if (data.results.length === 0) {
                    resultsList.innerHTML = '<li class="px-4 py-3 text-sm text-zinc-500 italic text-center">Nenhum produto encontrado.</li>';
                } else {
                    // Monta cada linha do dropdown
                    data.results.forEach(product => {
                        const li = document.createElement('li');
                        // Classe de estilo da linha do dropdown
                        li.className = 'px-4 py-3 hover:bg-zinc-800 cursor-pointer flex justify-between items-center transition-colors';
                        
                        // HTML interno da linha
                        li.innerHTML = `
                            <div>
                                <p class="text-sm font-medium text-zinc-200">${product.description}</p>
                                <p class="text-[10px] text-zinc-500 uppercase">Estoque: <span class="text-emerald-500 font-bold">${product.stock} un.</span></p>
                            </div>
                            <span class="text-sm font-mono text-zinc-400">R$ ${product.price}</span>
                        `;
                        
                        // Quando clicar na linha
                        li.onclick = () => selectProduct(product.id, product.description);
                        
                        resultsList.appendChild(li);
                    });
                }
                
                resultsList.classList.remove('hidden'); // Mostra a lista
            })
            .catch(error => console.error("Erro ao buscar produtos:", error));
    }, 300);
}

function selectProduct(id, description) {
    // Preenche o input escondido com o ID real
    document.getElementById('selected-product-id').value = id;
    
    // Preenche o input visível com o nome do produto
    document.getElementById('product-search-input').value = description;
    
    // Esconde a lista
    document.getElementById('product-search-results').classList.add('hidden');
    
    // Libera e colore o botão de submit
    const addBtn = document.getElementById('add-product-btn');
    addBtn.disabled = false;
    addBtn.className = 'bg-emerald-500 hover:bg-emerald-400 text-black font-bold px-4 py-2.5 rounded-lg transition-all shadow-lg shadow-emerald-500/20 cursor-pointer';
}

function disableAddButton(btn) {
    btn.disabled = true;
    btn.className = 'bg-zinc-800 text-zinc-500 font-bold px-4 py-2.5 rounded-lg transition-all border border-zinc-700 cursor-not-allowed';
}

// Fecha a lista suspensa se clicar fora dela
document.addEventListener('click', function(event) {
    const searchContainer = document.getElementById('product-search-input').parentElement;
    if (!searchContainer.contains(event.target)) {
        document.getElementById('product-search-results').classList.add('hidden');
    }
});