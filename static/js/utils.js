const showNavbar = () => {
    const navbarMobile = document.querySelector('.navbar-mobile');
    navbarMobile.classList.add('nav-show');
    navbarMobile.classList.remove('nav-hidden');
}
const hiddenNavbar = () => {
    const navbarMobile = document.querySelector('.navbar-mobile');
    navbarMobile.classList.add('nav-hidden');
    navbarMobile.classList.remove('nav-show');
}

const isMobile = () => {
    return window.screen.width < 600
}