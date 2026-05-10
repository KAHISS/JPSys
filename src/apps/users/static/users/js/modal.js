function openUserModal(button) {
    const data = button.dataset;

    // Se tiver nome completo, usa no título. Se não, usa o username.
    const title = (data.fullname && data.fullname.trim() !== '') ? data.fullname : data.username;
    document.getElementById('modal-user-title').textContent = title;
    
    document.getElementById('modal-user-username').textContent = data.username;
    document.getElementById('modal-user-type').textContent = data.type;
    document.getElementById('modal-user-phone').textContent = data.phone;
    document.getElementById('modal-user-document').textContent = data.document;
    
    // Junta endereço e cidade de forma elegante
    let addressFull = data.address;
    if (data.city !== '-') {
        addressFull = addressFull !== '-' ? `${data.address} - ${data.city}` : data.city;
    }
    document.getElementById('modal-user-address').textContent = addressFull;

    const modal = document.getElementById('user-modal');
    const modalBox = modal.querySelector('.transform');
    
    modalBox.classList.add('scale-95', 'opacity-0');
    modalBox.classList.remove('scale-100', 'opacity-100');
    modal.classList.remove('hidden');
    
    setTimeout(() => {
        modalBox.classList.add('scale-100', 'opacity-100');
        modalBox.classList.remove('scale-95', 'opacity-0');
    }, 10);
}

function closeUserModal() {
    const modal = document.getElementById('user-modal');
    const modalBox = modal.querySelector('.transform');
    
    modalBox.classList.remove('scale-100', 'opacity-100');
    modalBox.classList.add('scale-95', 'opacity-0');
    
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 200);
}

// Global: Fecha com ESC (Verifica qual modal está aberto)
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        const userModal = document.getElementById('user-modal');
        
        if (userModal && !userModal.classList.contains('hidden')) {
            closeUserModal();
        }
    }
});