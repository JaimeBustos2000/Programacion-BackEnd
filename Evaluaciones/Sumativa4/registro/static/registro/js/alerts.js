document.addEventListener('DOMContentLoaded', function () {
    var errorMessageElement = document.getElementById('errorMessage');
    if (errorMessageElement) {
        alert(errorMessageElement.textContent);
    }
});