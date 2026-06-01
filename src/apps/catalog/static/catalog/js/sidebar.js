document.addEventListener('DOMContentLoaded', () => {
    // --- CONTROLE DA SIDEBAR MOBILE ---
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const closeSidebarBtn = document.getElementById('closeSidebarBtn');
    const mobileSidebar = document.getElementById('mobileSidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    // Função para abrir o menu
    function openSidebar() {
        sidebarOverlay.classList.remove('hidden');
        // Pequeno delay para a animação do Tailwind funcionar
        setTimeout(() => {
            sidebarOverlay.classList.remove('opacity-0');
            mobileSidebar.classList.remove('-translate-x-full');
        }, 10);
        document.body.style.overflow = 'hidden'; // Evita que a página role por trás
    }

    // Função para fechar o menu
    function closeSidebar() {
        mobileSidebar.classList.add('-translate-x-full');
        sidebarOverlay.classList.add('opacity-0');
        // Aguarda a transição antes de sumir com o elemento
        setTimeout(() => {
            sidebarOverlay.classList.add('hidden');
            document.body.style.overflow = ''; // Restaura a rolagem
        }, 300);
    }

    // Event Listeners
    mobileMenuBtn.addEventListener('click', openSidebar);
    closeSidebarBtn.addEventListener('click', closeSidebar);
    
    // Fechar ao clicar na parte escura fora do menu
    sidebarOverlay.addEventListener('click', closeSidebar);
});
