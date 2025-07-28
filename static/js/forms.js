// JavaScript partagé pour les formulaires de connexion et d'inscription

document.addEventListener('DOMContentLoaded', function() {
    // Ajouter la classe field-error aux champs avec des erreurs
    const errorFields = document.querySelectorAll('.text-danger');
    errorFields.forEach(function(errorField) {
        const field = errorField.previousElementSibling;
        if (field && field.classList.contains('form-control')) {
            field.classList.add('field-error');
        }
    });

    // Validation en temps réel pour les formulaires
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Supprimer la classe field-error quand l'utilisateur commence à taper
    const formControls = document.querySelectorAll('.form-control');
    formControls.forEach(function(control) {
        control.addEventListener('input', function() {
            if (this.classList.contains('field-error')) {
                this.classList.remove('field-error');
            }
        });
    });
});
