document.getElementById('caracteristicas-filter').addEventListener('click', function () {
    const selectElement = document.getElementById('caracteristica');
    const selectedOption = selectElement.options[selectElement.selectedIndex];

    if (selectedOption.value !== "") {
        const tagContainer = document.getElementById('tags-container');
        const existingTags = tagContainer.querySelectorAll('.tag-item');

        let tagExists = false;
        existingTags.forEach(function (tag) {
            if (tag.getAttribute('data-id') === selectedOption.value) {
                tagExists = true;
            }
        });

        if (!tagExists) {
            const tagDiv = document.createElement('div');
            tagDiv.className = 'tag-item';
            tagDiv.setAttribute('data-id', selectedOption.value);
            tagDiv.innerHTML = `${selectedOption.text} <span class="remove-tag" style="cursor:pointer;">&times;</span>`;
            tagContainer.appendChild(tagDiv);

            // Desactivar la opción seleccionada
            selectedOption.disabled = true;

            // Actualizar el campo oculto con los IDs de las características seleccionadas
            updateHiddenInput();

            tagDiv.querySelector('.remove-tag').addEventListener('click', function () {
                tagContainer.removeChild(tagDiv);
                selectedOption.disabled = false;

                // Actualizar el campo oculto al eliminar
                updateHiddenInput();
            });
        } else {
            alert("Esta característica ya ha sido añadida.");
        }
    }
});

// Función para actualizar el campo oculto con los IDs de las características seleccionadas
function updateHiddenInput() {
    const tagContainer = document.getElementById('tags-container');
    const tagItems = tagContainer.querySelectorAll('.tag-item');
    const selectedIds = Array.from(tagItems).map(tag => tag.getAttribute('data-id')).join(',');

    document.getElementById('caracteristicas_ids').value = selectedIds;
}


