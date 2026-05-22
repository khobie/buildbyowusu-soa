document.addEventListener('DOMContentLoaded', () => {
    // Page loader
    const loader = document.getElementById('page-loader');
    if (loader) {
        window.addEventListener('load', () => {
            setTimeout(() => loader.classList.add('hidden'), 300);
        });
    }

    // AOS
    if (typeof AOS !== 'undefined') {
        AOS.init({ duration: 700, once: true, offset: 80 });
    }

    // Animated counters
    const counters = document.querySelectorAll('[data-count]');
    const animateCounter = (el) => {
        const target = parseInt(el.dataset.count, 10);
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        const update = () => {
            current += step;
            if (current < target) {
                el.textContent = Math.floor(current).toLocaleString();
                requestAnimationFrame(update);
            } else {
                el.textContent = target.toLocaleString();
            }
        };
        update();
    };

    if (counters.length && 'IntersectionObserver' in window) {
        const obs = new IntersectionObserver((entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    animateCounter(e.target);
                    obs.unobserve(e.target);
                }
            });
        }, { threshold: 0.5 });
        counters.forEach(c => obs.observe(c));
    }

    // Testimonial carousel
    const carousel = document.getElementById('testimonialCarousel');
    if (carousel && typeof bootstrap !== 'undefined') {
        new bootstrap.Carousel(carousel, { interval: 5000 });
    }

    // Lazy images
    document.querySelectorAll('img[data-src]').forEach(img => {
        const obs = new IntersectionObserver(entries => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    obs.unobserve(img);
                }
            });
        });
        obs.observe(img);
    });
});
