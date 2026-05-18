// Adiciona o evento de mudança no select de promotores do modal
document.querySelector('select[name="promoter_id"]').addEventListener('change', async function() {
    const promoterId = this.value;
    const productId = document.getElementById('dispatch-product-id').value;
    
    const pricingFields = document.getElementById('pricing-fields');
    const salePriceInput = document.querySelector('input[name="sale_price"]');
    const serviceFeeInput = document.querySelector('input[name="service_fee"]');

    // Se o usuário voltar a opção para "Selecione...", reseta a tela
    if (!promoterId) {
        pricingFields.classList.remove('hidden');
        salePriceInput.required = true;
        serviceFeeInput.required = true;
        return;
    }

    try {
        // Vai no Django perguntar se o estoque já existe
        const response = await fetch(`/inventory/promoters/inventory/check?product_id=${productId}&promoter_id=${promoterId}`);
        const data = await response.json();

        if (data.exists) {
            // Se JÁ TEM: Esconde a div, tira o 'required' e limpa os valores
            salePriceInput.value = data.sale_price;
            serviceFeeInput.value = data.service_fee;
        } else {
            salePriceInput.value = data.sale_price
        }
    } catch (error) {
        console.error("Erro ao verificar estoque:", error);
    }
});