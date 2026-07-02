function toastMessage(message, type = 'success') {
    const colors = {
        success: 'text-green-300',
        error: 'text-red-300',
        warning: 'text-yellow-300',
        info: 'text-blue-300'
    };

    const toast = document.createElement('div');

    toast.className = `
        fixed top-5 right-5 text-white px-6 py-3 rounded-lg shadow-lg
        transition-all duration-300 translate-x-full opacity-0 bg-zinc-900 border-2 border-amber-500
        ${colors[type]}
    `;

    toast.textContent = message;

    document.getElementById("header").appendChild(toast);

    setTimeout(() => {
        toast.classList.remove('translate-x-full', 'opacity-0');
    }, 10);

    setTimeout(() => {
        toast.classList.add('translate-x-full', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

export { toastMessage }