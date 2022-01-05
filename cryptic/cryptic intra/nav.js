let navBtn = document.querySelector('.toggleNav');
let nav = document.querySelector('.navbar-responsive');
let navLinks = document.querySelectorAll('.navbar-responsive__link')

navBtn.addEventListener('click', () => {
    if (navBtn.classList.contains('close')) {
        navBtn.classList.remove('close');
    } else {
        navBtn.classList.add('close');
    }

    if (nav.classList.contains('open')) {
        nav.classList.remove('open');
    } else {
        nav.classList.add('open');
    }

    navLinks.forEach((link) => {
        if (link.classList.contains('open__link')) {
            link.classList.remove('open__link');
        } else {
            link.classList.add('open__link');
        }
    })
})