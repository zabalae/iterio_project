document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('register-form');
    const popupContainer = document.getElementById('popup-container');
    const registerContainer = document.getElementById('register-container');
    const body = document.body;

    form.addEventListener('submit', function(event) {
        // Prevent form submission
        event.preventDefault();

        // Check if all required fields are filled
        const username = document.getElementById('id_username').value.trim();
        const email = document.getElementById('id_email').value.trim();
        const firstName = document.getElementById('id_first_name').value.trim();
        const lastName = document.getElementById('id_last_name').value.trim();
        const password1 = document.getElementById('id_password1').value.trim();
        const password2 = document.getElementById('id_password2').value.trim();

        // Remove any existing error messages
        const errorMessages = form.querySelectorAll('.text-red-600');
        errorMessages.forEach(function(element) {
            element.style.display = 'none';
        });

        // Check if any required field is empty
        let formValid = true;
        if (username === '') {
            document.getElementById('id_username_error').style.display = 'block';
            formValid = false;
        }
        if (email === '') {
            document.getElementById('id_email_error').style.display = 'block';
            formValid = false;
        }
        if (firstName === '') {
            document.getElementById('id_first_name_error').style.display = 'block';
            formValid = false;
        }
        if (lastName === '') {
            document.getElementById('id_last_name_error').style.display = 'block';
            formValid = false;
        }
        if (password1 === '') {
            document.getElementById('id_password1_error').style.display = 'block';
            formValid = false;
        }
        if (password2 === '') {
            document.getElementById('id_password2_error').style.display = 'block';
            formValid = false;
        }

        // If form is valid, proceed with submission actions
        if (formValid) {
            popupContainer.classList.remove('hidden');
            registerContainer.classList.add('dimmed');
            registerContainer.classList.add('no-interact');
            body.classList.add('no-scroll');

            // Submit the form (optional, depending on your needs)
            // form.submit();
        }
    });
});
