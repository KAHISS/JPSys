// Lógica do Menu Hambúrguer
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('sidebar-overlay');
const section = document.getElementById('section')

function toggleSidebar() {
    sidebar.classList.toggle('-translate-x-full');
    overlay.classList.toggle('hidden');
}

// Adiciona estilos ativos ao botão clicado
const btn = document.querySelector(`.${section.textContent}`);
btn.classList.remove('text-zinc-400', 'hover:bg-zinc-900', 'hover:text-amber-400');
btn.classList.add('bg-amber-500', 'text-black', 'shadow-lg', 'shadow-amber-500/20');

// 5. Fechar sidebar no mobile após clicar
if (window.innerWidth < 768) {
    toggleSidebar();
}