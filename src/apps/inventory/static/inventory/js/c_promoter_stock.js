document.getElementById('form-dispatch-stock').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const dataObj = {
        product_id: formData.get('product_id'),
        promoter_id: formData.get('promoter_id'),
        quantity: parseInt(formData.get('quantity'))
    };

    try {
        const response = await fetch('/inventory/api/dispatch-stock/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            },
            body: JSON.stringify(dataObj)
        });

        const result = await response.json();

        if (response.ok) {
            alert("Estoque transferido com sucesso!");
            closeDispatchModal();
            location.reload(); // Recarrega a página para atualizar o número do estoque principal na tabela
        } else {
            alert(result.error || "Erro ao transferir estoque.");
        }
    } catch (error) {
        alert("Erro de conexão.");
    }
});