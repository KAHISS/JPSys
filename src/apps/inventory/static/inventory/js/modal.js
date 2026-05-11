function openProductModal(button) {
    const data = button.dataset;

    document.getElementById('modal-title').textContent = data.description;
    document.getElementById('modal-barcode').textContent = data.barcode;
    document.getElementById('modal-type').textContent = data.type;
    document.getElementById('modal-category').textContent = data.category;
    document.getElementById('modal-stock').textContent = data.stock;
    document.getElementById('modal-cost').textContent = 'R$ ' + data.cost;
    document.getElementById('modal-price').textContent = 'R$ ' + data.price;

    const imgElement = document.getElementById('modal-image');
    const noImgElement = document.getElementById('modal-no-image');

    if (data.image !== 'no-image') {
        imgElement.src = data.image;
        imgElement.classList.remove('hidden');
        noImgElement.classList.add('hidden');
    } else {
        imgElement.src = '';
        imgElement.classList.add('hidden');
        noImgElement.classList.remove('hidden');
    }

    const modal = document.getElementById('product-modal');
    const modalBox = modal.querySelector('.transform');
    
    // Garante o estado inicial recolhido antes de mostrar
    modalBox.classList.add('scale-95', 'opacity-0');
    modalBox.classList.remove('scale-100', 'opacity-100');
    
    modal.classList.remove('hidden');
    
    // Ativa a animação de entrada
    setTimeout(() => {
        modalBox.classList.add('scale-100', 'opacity-100');
        modalBox.classList.remove('scale-95', 'opacity-0');
    }, 10);
}

function closeProductModal() {
    const modal = document.getElementById('product-modal');
    const modalBox = modal.querySelector('.transform');
    
    // Inicia a animação de saída (encolhendo e sumindo)
    modalBox.classList.remove('scale-100', 'opacity-100');
    modalBox.classList.add('scale-95', 'opacity-0');
    
    // Espera a animação terminar (200ms) para esconder o container
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 200);
}

// --- Lógica do Modal de Categoria ---
function openCategoryModal() {
    const modal = document.getElementById('category-modal');
    const modalBox = modal.querySelector('.transform');
    document.getElementById('new_category_name').value = ''; // Limpa o input
    
    modalBox.classList.add('scale-95', 'opacity-0');
    modalBox.classList.remove('scale-100', 'opacity-100');
    modal.classList.remove('hidden');
    
    setTimeout(() => {
        modalBox.classList.add('scale-100', 'opacity-100');
        modalBox.classList.remove('scale-95', 'opacity-0');
        document.getElementById('new_category_name').focus();
    }, 10);
}

function closeCategoryModal() {
    const modal = document.getElementById('category-modal');
    const modalBox = modal.querySelector('.transform');
    
    modalBox.classList.remove('scale-100', 'opacity-100');
    modalBox.classList.add('scale-95', 'opacity-0');
    setTimeout(() => modal.classList.add('hidden'), 200);
}

function openDispatchModal(button) {
    const data = button.dataset;
    document.getElementById('pricing-fields').classList.remove('hidden');
    document.querySelector('input[name="sale_price"]').required = true;
    document.querySelector('input[name="service_fee"]').required = true;
    document.querySelector('select[name="promoter_id"]').value = '';
    document.getElementById('dispatch-product-id').value = data.id;
    document.getElementById('dispatch-product-name').textContent = data.name;
    document.getElementById('dispatch-current-stock').textContent = data.stock;
    
    // Configura o valor máximo do input para não deixar enviar mais do que tem no estoque principal
    document.getElementById('dispatch-quantity').max = data.stock;
    document.getElementById('dispatch-quantity').value = '';

    const modal = document.getElementById('dispatch-modal');
    const modalBox = modal.querySelector('.transform');
    
    modalBox.classList.add('scale-95', 'opacity-0');
    modalBox.classList.remove('scale-100', 'opacity-100');
    modal.classList.remove('hidden');
    
    setTimeout(() => {
        modalBox.classList.add('scale-100', 'opacity-100');
        modalBox.classList.remove('scale-95', 'opacity-0');
    }, 10);
}

function closeDispatchModal() {
    const modal = document.getElementById('dispatch-modal');
    const modalBox = modal.querySelector('.transform');
    modalBox.classList.remove('scale-100', 'opacity-100');
    modalBox.classList.add('scale-95', 'opacity-0');
    setTimeout(() => modal.classList.add('hidden'), 200);
}

function openReturnModal(button) {
    const data = button.dataset;
    
    // Preenche os campos do modal com os dados do botão (data-*)
    document.getElementById('return-stock-id').value = data.id;
    document.getElementById('return-product-name').textContent = data.product;
    document.getElementById('return-promoter-name').textContent = data.promoter;
    document.getElementById('return-available-qty').textContent = data.max;
    
    // Define o limite máximo que pode ser digitado no input
    const qtyInput = document.getElementById('return-quantity');
    qtyInput.max = data.max;
    qtyInput.value = ''; // Limpa o campo para o novo preenchimento

    const modal = document.getElementById('return-stock-modal');
    const modalBox = modal.querySelector('.transform');
    
    // Animação de entrada
    modal.classList.remove('hidden');
    setTimeout(() => {
        modalBox.classList.add('scale-100', 'opacity-100');
        modalBox.classList.remove('scale-95', 'opacity-0');
        qtyInput.focus();
    }, 10);
}

function closeReturnModal() {
    const modal = document.getElementById('return-stock-modal');
    const modalBox = modal.querySelector('.transform');
    
    // Animação de saída
    modalBox.classList.remove('scale-100', 'opacity-100');
    modalBox.classList.add('scale-95', 'opacity-0');
    
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 200);
}