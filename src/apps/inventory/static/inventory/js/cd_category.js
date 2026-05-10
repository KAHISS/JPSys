document.getElementById('form-new-category').addEventListener('submit', async (event) => {
    event.preventDefault(); 
    
    const formData = new FormData(event.target);
    const nome = formData.get('name');
    const csrfToken = formData.get('csrfmiddlewaretoken');

    try {
        const response = await fetch('/inventory/create/category/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ name: nome, action: "create" })
        });

        if (response.ok) {
            const data = await response.json();
            
            const select = document.getElementById('id_category');
            const newOption = new Option(data.name, data.id, false, true);
            select.add(newOption);
            
            closeCategoryModal();
            event.target.reset(); 
        } else {
            alert("Erro ao criar a categoria.");
        }
    } catch (error) {
        console.error('Erro:', error);
        alert("Erro de conexão.");
    }
});

document.getElementById('delete-btn').addEventListener('click', async (event) => {
    event.preventDefault(); 
    
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    console.log(csrfToken)
    const id = document.getElementById("id_category").value
    const option = document.querySelector(`option[value="${id}"]`)


    if (confirm(`Ao deletar a categoria "${option.textContent}", todos produtos que a usam ficaram sem categoria. Essa ação não pode ser desfeita`)) {
        try {
            const response = await fetch('/inventory/delete/category/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ id: id, action: "delete"})
            });
            
            if (response.ok) {
                const data = await response.json();
                option.remove()
            } else {
                alert("Erro ao deletar a categoria.");
            }
        } catch (error) {
            console.error('Erro:', error);
            alert("Erro de conexão.");
        }
    }
});