document.addEventListener('DOMContentLoaded', function () {
    var menuToggle = document.getElementById('menuToggle');
    var backgroundOverlay = document.querySelector('.background-overlay');
    var dropdown = document.querySelector('.dropdown');

    menuToggle.addEventListener('change', function () {
        if (this.checked) {
            document.body.classList.add('menu-open');
            document.body.classList.remove('menu-open-full');
            dropdown.classList.remove('slide-out');
        } else {
            document.body.classList.remove('menu-open');
            dropdown.classList.add('slide-out');
        }
    });

    backgroundOverlay.addEventListener('click', function () {
        menuToggle.checked = false;
        dropdown.classList.add('slide-out');
    });

    dropdown.addEventListener('animationend', function (event) {
        if (event.animationName === 'slideOut' && !menuToggle.checked) {
            document.body.classList.remove('menu-open');
            document.body.classList.remove('menu-open-full');
            dropdown.classList.remove('slide-out');
        }
    });

    document.body.addEventListener('click', function (event) {
        if (!dropdown.contains(event.target) && !menuToggle.contains(event.target)) {
            menuToggle.checked = false;
            dropdown.classList.add('slide-out');
        }
    });
});

function highlightButton(button) {
    button.style.backgroundColor = "#27ae60";
}

function resetButtonColor(button) {
    button.style.backgroundColor = "#3498db";
}

function redirectToHome() {
    window.location.href = "https://hoshiyuki-api.my.id";
}

