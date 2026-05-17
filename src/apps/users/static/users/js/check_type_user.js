document.addEventListener("DOMContentLoaded", function () {
        const typeSelect = document.getElementById("id_type");
        const commissionContainer = document.getElementById("commission-container");

        function toggleCommission() {
            // Verifica se o valor selecionado é 'promoter'
            if (typeSelect && typeSelect.value === "promoter") {
                commissionContainer.classList.remove("hidden");
            } else {
                commissionContainer.classList.add("hidden");
                
                // Opcional: Limpa o valor se mudar para outro tipo que não seja promotor
                const commissionInput = commissionContainer.querySelector("input");
                if (commissionInput && !typeSelect.form.dataset.isUpdate) { 
                    commissionInput.value = ""; 
                }
            }
        }

        if (typeSelect) {
            // Executa ao carregar a página (caso seja edição e já seja promotor)
            toggleCommission();

            // Executa sempre que o usuário mudar a opção do select
            typeSelect.addEventListener("change", toggleCommission);
        }
    });