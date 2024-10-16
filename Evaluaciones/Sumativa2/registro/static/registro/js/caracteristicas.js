document.addEventListener('DOMContentLoaded', function () {
    function addCaracteristica() {
        const container = document.getElementById('caracteristicas-container');
        const newCaracteristica = document.createElement('div');
        newCaracteristica.classList.add('caracteristica');

        // Generar las opciones del select a partir de la lista de características
        let optionsHTML = '';
        if (Array.isArray(listaCaracteristicas_json)) {
            listaCaracteristicas_json.forEach(caracteristica => {
                optionsHTML += `<option value="${caracteristica}">${caracteristica}</option>`;
            });
        } else {
            console.error('listaCaracteristicas_json no es un array:', listaCaracteristicas_json);
        }

        newCaracteristica.innerHTML = `
        <label class="labels">Nombre:</label>
        <select name="caracteristicas_nombre[]" class="inputs" required>
            ${optionsHTML}
        </select>
        <label class="labels">Detalle:</label>
        <input type="text" name="caracteristicas_detalle[]" class="inputs" minlength="3" required>
        <button type="button" class="btn-remove" onclick="removeCaracteristica(this)">Eliminar</button>
    `;
        container.appendChild(newCaracteristica);

        // Attach event listener to the new remove button
        newCaracteristica.querySelector('.btn-remove').addEventListener('click', function () {
            removeCaracteristica(this);
        });
    }

    function removeCaracteristica(button) {
        const caracteristica = button.parentElement;
        caracteristica.remove();
    }

    // Attach event listener to the add button
    document.querySelector('.btn-add').addEventListener('click', addCaracteristica);

    // Attach event listeners to existing remove buttons
    document.querySelectorAll('.btn-remove').forEach(button => {
        button.addEventListener('click', function () {
            removeCaracteristica(this);
        });
    });
});
