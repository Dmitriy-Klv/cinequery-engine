document.addEventListener("DOMContentLoaded", function () {
    const images = [
        "/static/images/bg1.jpg",
        "/static/images/bg2.jpg",
        "/static/images/bg3.jpg",
        "/static/images/bg4.jpg",
        "/static/images/bg5.jpg",
        "/static/images/bg6.jpg",
        "/static/images/bg7.jpg",
        "/static/images/bg8.jpg",
        "/static/images/bg9.jpg",
        "/static/images/bg10.jpg",
        "/static/images/bg11.jpg"
    ];

    let currentIndex = 1;
    const body = document.body;

    function preloadImages() {
        images.forEach(src => {
            const img = new Image();
            img.src = src;
        });
    }
    function setInitialBackground() {
        const firstImage = `url('${images[0]}')`;
        body.style.setProperty('--current-bg', firstImage);
    }

    function changeBackground() {
        const nextImage = `url('${images[currentIndex]}')`;

        body.style.setProperty('--next-bg', nextImage);

        body.classList.add("bg-fade");

        setTimeout(() => {
            body.style.setProperty('--current-bg', nextImage);
            body.classList.remove("bg-fade");
        }, 1500);

        currentIndex = (currentIndex + 1) % images.length;
    }

    preloadImages();
    setInitialBackground();

    setTimeout(() => {
        changeBackground();
        setInterval(changeBackground, 10000);
    }, 2000);
});