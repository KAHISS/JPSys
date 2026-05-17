document.addEventListener('DOMContentLoaded', function() {
        // O Django sempre cria os inputs com o prefixo "id_"
        const serviceCheckbox = document.getElementById('id_service');
        const clientSection = document.getElementById('client-data-section');

        // Pega os campos para podermos limpá-los caso o usuário desmarque a caixa
        const nameInput = document.getElementById('id_customer_name');
        const cpfInput = document.getElementById('id_customer_cpf');
        const birthInput = document.getElementById('id_customer_birth_date');
        const feeInput = document.getElementById('id_service_fee_sold');

        function toggleClientFields() {
            if (serviceCheckbox.checked) {
                // Se marcou que tem serviço, MOSTRA o bloco do cliente
                clientSection.classList.remove('hidden');
                clientSection.classList.add('block');
                
                // Opcional: Se quiser que o nome seja obrigatório ao marcar, descomente a linha abaixo:
                // nameInput.required = true;
            } else {
                // Se desmarcou, ESCONDE o bloco do cliente
                clientSection.classList.add('hidden');
                clientSection.classList.remove('block');
                
                // Limpa os campos para não enviar lixo pro banco de dados sem querer
                if(nameInput) nameInput.value = '';
                if(cpfInput) cpfInput.value = '';
                if(birthInput) birthInput.value = '';
                if(feeInput) feeInput.value = '0.00'; // Zera a taxa de serviço
                
                // Remove a obrigatoriedade caso tenha adicionado
                // nameInput.required = false;
            }
        }

        if (serviceCheckbox) {
            // Roda a função assim que a página carrega (importante para quando for a tela de "Editar Venda")
            toggleClientFields();

            // Fica "ouvindo" toda vez que o usuário clica no checkbox
            serviceCheckbox.addEventListener('change', toggleClientFields);
        }
    });