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
    
    modalBox.classList.add('scale-95', 'opacity-0');
    modalBox.classList.remove('scale-100', 'opacity-100');
    
    modal.classList.remove('hidden');
    
    setTimeout(() => {
        modalBox.classList.add('scale-100', 'opacity-100');
        modalBox.classList.remove('scale-95', 'opacity-0');
    }, 10);
}

function closeProductModal() {
    const modal = document.getElementById('product-modal');
    const modalBox = modal.querySelector('.transform');
    
    modalBox.classList.remove('scale-100', 'opacity-100');
    modalBox.classList.add('scale-95', 'opacity-0');
    
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 200);
}

function openCategoryModal() {
    const modal = document.getElementById('category-modal');
    const modalBox = modal.querySelector('.transform');
    document.getElementById('new_category_name').value = '';
    
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
    document.getElementById('return-stock-id').value = data.id;
    document.getElementById('return-product-name').textContent = data.product;
    document.getElementById('return-promoter-name').textContent = data.promoter;
    document.getElementById('return-available-qty').textContent = data.max;
    
    const qtyInput = document.getElementById('return-quantity');
    qtyInput.max = data.max;
    qtyInput.value = '';

    const modal = document.getElementById('return-stock-modal');
    const modalBox = modal.querySelector('.transform');
    
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
    modalBox.classList.remove('scale-100', 'opacity-100');
    modalBox.classList.add('scale-95', 'opacity-0');
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 200);
}

function openSaleDetailsModal(button) {
    const data = button.dataset;
    document.getElementById('modal-sale-iccid').textContent = data.iccid;
    document.getElementById('modal-sale-date').textContent = data.date;
    document.getElementById('modal-sale-product').textContent = data.product;
    document.getElementById('modal-sale-promoter').textContent = data.promoter;
    document.getElementById('modal-sale-price').textContent = `R$ ${data.price}`;
    document.getElementById('modal-sale-fee').textContent = `R$ ${data.fee}`;
    document.getElementById('modal-sale-total').textContent = `R$ ${data.total}`;
    
    const serviceBadge = document.getElementById('modal-sale-service-badge');

    if (data.service === 'True') {
        serviceBadge.textContent = 'SIM';
        serviceBadge.className = 'ml-1 text-[9px] px-1.5 py-0.5 bg-emerald-500/20 text-emerald-400 rounded';
    } else {
        serviceBadge.textContent = 'NÃO';
        serviceBadge.className = 'ml-1 text-[9px] px-1.5 py-0.5 bg-zinc-800 text-zinc-500 rounded';
    }

    const modal = document.getElementById('sale-details-modal');
    const modalBox = modal.querySelector('.transform');
    
    modalBox.classList.add('scale-95', 'opacity-0');
    modalBox.classList.remove('scale-100', 'opacity-100');
    modal.classList.remove('hidden');
    
    setTimeout(() => {
        modalBox.classList.add('scale-100', 'opacity-100');
        modalBox.classList.remove('scale-95', 'opacity-0');
    }, 10);
}

function closeSaleDetailsModal() {
    const modal = document.getElementById('sale-details-modal');
    const modalBox = modal.querySelector('.transform');
    modalBox.classList.remove('scale-100', 'opacity-100');
    modalBox.classList.add('scale-95', 'opacity-0');
    setTimeout(() => modal.classList.add('hidden'), 200);
}

function openOrderModal(button) {
    const id = button.dataset.id;
    const date = button.dataset.date;
    const client = button.dataset.client;
    const status = button.dataset.status;
    const quantity = button.dataset.quantity;
    const total = button.dataset.total;
    let obs = button.dataset.obs;

    if (!obs || obs.trim() === '' || obs === 'None') {
        obs = "Nenhuma observação registrada neste pedido.";
    }

    document.getElementById('modal-order-id').innerText = id;
    document.getElementById('modal-order-date').innerText = date;
    document.getElementById('modal-order-client').innerText = client;
    document.getElementById('modal-order-status').innerText = status;
    document.getElementById('modal-order-quantity').innerText = quantity + " un.";
    document.getElementById('modal-order-total').innerText = "R$ " + total;
    document.getElementById('modal-order-obs').innerText = obs;

    document.getElementById('order-details-modal').classList.remove('hidden');
}

function closeOrderModal() {
    document.getElementById('order-details-modal').classList.add('hidden');
}

function openEditItemModal(button) {
    const itemId = button.dataset.id;
    const productName = button.dataset.product;
    const currentQty = button.dataset.quantity;
    const url = button.dataset.url;
    
    const form = document.getElementById('edit-item-form');
    form.action = url;

    document.getElementById('modal-item-product').innerText = productName;
    document.getElementById('modal-item-quantity').value = currentQty;

    document.getElementById('edit-item-modal').classList.remove('hidden');
    
    setTimeout(() => document.getElementById('modal-item-quantity').focus(), 100);
}

function closeEditItemModal() {
    document.getElementById('edit-item-modal').classList.add('hidden');
}

function openAddressModal(button = null) {
    const modal = document.getElementById('address-modal');
    const modalBox = modal.querySelector('.transform');
    const form = document.getElementById('form-new-address');
    const title = document.getElementById('modal-address-title');

    if (form) {
        form.reset();
    }

    if (button) {
        const data = button.dataset;
        title.textContent = data.title || 'Editar Endereço';
        form.action = data.url;

        const fields = {
            address: document.getElementById('id_address'),
            number: document.getElementById('id_number'),
            complement: document.getElementById('id_complement'),
            neighborhood: document.getElementById('id_neighborhood'),
            cep: document.getElementById('id_cep'),
            city: document.getElementById('id_city'),
        };

        if (fields.address) fields.address.value = data.address || '';
        if (fields.number) fields.number.value = data.number || '';
        if (fields.complement) fields.complement.value = data.complement || '';
        if (fields.neighborhood) fields.neighborhood.value = data.neighborhood || '';
        if (fields.cep) fields.cep.value = data.cep || '';
        if (fields.city) fields.city.value = data.city || '';
    } else {
        title.textContent = 'Novo Endereço';
        form.action = form.getAttribute('action');
    }

    modalBox.classList.add('scale-95', 'opacity-0');
    modalBox.classList.remove('scale-100', 'opacity-100');
    modal.classList.remove('hidden');

    setTimeout(() => {
        modalBox.classList.add('scale-100', 'opacity-100');
        modalBox.classList.remove('scale-95', 'opacity-0');
        const firstInput = document.getElementById('id_address');
        if (firstInput) firstInput.focus();
    }, 10);
}

function closeAddressModal() {
    const modal = document.getElementById('address-modal');
    const modalBox = modal.querySelector('.transform');

    modalBox.classList.remove('scale-100', 'opacity-100');
    modalBox.classList.add('scale-95', 'opacity-0');

    setTimeout(() => {
        modal.classList.add('hidden');
    }, 200);
}
