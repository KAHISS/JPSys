document.addEventListener('DOMContentLoaded', () => {
    const mobileSearchBtn = document.getElementById('mobileSearchBtn');
    const closeMobileSearchBtn = document.getElementById('closeMobileSearchBtn');
    const mobileSearchBar = document.getElementById('mobileSearchBar');
    const mobileSearchInput = document.getElementById('mobileSearchInput');

    // Função para abrir a pesquisa mobile
    mobileSearchBtn.addEventListener('click', () => {
        mobileSearchBar.classList.remove('hidden');
        // Pequeno delay para a transição do Tailwind funcionar corretamente
        setTimeout(() => {
            mobileSearchBar.classList.remove('scale-y-0', 'opacity-0');
            mobileSearchBar.classList.add('scale-y-100', 'opacity-100');
            mobileSearchInput.focus();
        }, 10);
    });

    // Função para fechar a pesquisa mobile
    closeMobileSearchBtn.addEventListener('click', () => {
        mobileSearchBar.classList.remove('scale-y-100', 'opacity-100');
        mobileSearchBar.classList.add('scale-y-0', 'opacity-0');
        
        // Aguarda a transição terminar antes de ocultar o elemento
        setTimeout(() => {
            mobileSearchBar.classList.add('hidden');
            mobileSearchInput.value = ''; // Opcional: limpa o campo ao fechar
        }, 300);
    });
});