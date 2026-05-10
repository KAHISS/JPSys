// Lógica do Menu Hambúrguer
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('sidebar-overlay');

function toggleSidebar() {
    sidebar.classList.toggle('-translate-x-full');
    overlay.classList.toggle('hidden');
}

// 5. Fechar sidebar no mobile após clicar
if (window.innerWidth < 768) {
    toggleSidebar();
}