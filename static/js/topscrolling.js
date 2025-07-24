const topBtn = document.querySelector('.go-top');
// console.log(topBtn);

window.addEventListener('scroll', triggerScroll);

function triggerScroll() {
    if (window.scrollY > 100) {
        topBtn.style.display = 'block';
    } else {
        topBtn.style.display = 'none';
    }
}

topBtn.addEventListener('click', goTop);

function goTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}