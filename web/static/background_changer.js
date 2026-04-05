document.addEventListener("DOMContentLoaded", function() {
    const images = [
        "/static/images/bg1.jpg",
        "/static/images/bg2.jpg",
        "/static/images/bg3.jpg"
    ];

    let currentIndex = 0;
    const body = document.body;

    function changeBackground() {
        const gradient = "linear-gradient(180deg, rgba(20, 20, 20, 0.3) 0%, rgba(20, 20, 20, 0.6) 100%)";
        body.style.backgroundImage = `${gradient}, url('${images[currentIndex]}')`;
        currentIndex = (currentIndex + 1) % images.length;
    }

    changeBackground();
    setInterval(changeBackground, 5000);
});