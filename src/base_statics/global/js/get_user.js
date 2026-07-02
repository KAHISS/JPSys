// Variável para evitar mandar dezenas de requisições se o usuário digitar muito rápido [cite: 1]
let searchClientTimeout = null;

function searchClients(query) {
    const resultsList = document.getElementById('client-search-results');

    // Se apagar o texto, esconde a lista e bloqueia o botão [cite: 3]
    if (query.trim().length < 2) {
        resultsList.classList.add('hidden');
        resultsList.innerHTML = '';
        document.getElementById('selected-client-id').value = '';
        return;
    }

    clearTimeout(searchClientTimeout);

    // Espera 300ms após o usuário parar de digitar para fazer a busca [cite: 5]
    searchClientTimeout = setTimeout(() => {
        // Ajuste a URL para apontar para a sua view de clientes
        fetch(`/users/search-clients/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                resultsList.innerHTML = ''; // Limpa a lista [cite: 6]
                
                if (data.results.length === 0) {
                    resultsList.innerHTML = '<li class="px-4 py-3 text-sm text-zinc-500 italic text-center">Nenhum cliente encontrado.</li>';
                } else {
                    // Monta cada linha do dropdown [cite: 7]
                    data.results.forEach(client => {
                        const li = document.createElement('li');
                        li.className = 'px-4 py-3 hover:bg-zinc-800 cursor-pointer flex justify-between items-center transition-colors';
                        
                        // HTML interno da linha com tema escuro e dourado/âmbar [cite: 9]
                        li.innerHTML = `
                            <div>
                                <p class="text-sm font-medium text-zinc-200">${client.name}</p>
                                <p class="text-[10px] text-zinc-500 uppercase">Tel: <span class="text-amber-500 font-bold">${client.phone}</span></p>
                            </div>
                            <span class="text-sm font-mono text-zinc-400">${client.document}</span>
                        `;
                        
                        // Quando clicar na linha [cite: 12]
                        li.onclick = () => selectClient(client.id, client.name);
                        resultsList.appendChild(li);
                    });
                }
                
                resultsList.classList.remove('hidden'); // Mostra a lista [cite: 14]
            })
            .catch(error => console.error("Erro ao buscar clientes:", error));
    }, 300);
}

function selectClient(id, name) {
    // Preenche o input escondido com o ID real [cite: 15]
    document.getElementById('selected-client-id').value = id;
    // Preenche o input visível com o nome [cite: 16]
    document.getElementById('client-search-input').value = name;
    // Esconde a lista [cite: 17]
    document.getElementById('client-search-results').classList.add('hidden');
    
}

// Fecha a lista suspensa se clicar fora dela [cite: 20]
document.addEventListener('click', function(event) {
    const searchInput = document.getElementById('client-search-input');
    if (searchInput) {
        const searchContainer = searchInput.parentElement;
        if (!searchContainer.contains(event.target)) {
            document.getElementById('client-search-results').classList.add('hidden');
        }
    }
});