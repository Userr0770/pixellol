document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');

    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(registerForm);
            fetch(registerForm.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '{% url "login" %}';
                } else {
                    alert(data.error || 'Произошла ошибка. Попробуйте позже.');
                }
            })
            .catch(error => {
                alert('Произошла ошибка. Попробуйте позже.');
            });
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(loginForm);
            fetch(loginForm.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '{% url "home" %}';
                } else {
                    alert(data.error || 'Неверный логин или пароль.');
                }
            })
            .catch(error => {
                alert('Произошла ошибка. Попробуйте позже.');
            });
        });
    }
});