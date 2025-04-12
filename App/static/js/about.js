// about.js – Carousel + Redirect Button

document.addEventListener('DOMContentLoaded', () => {
    console.log("✅ about.js loaded and running!");

    // Get elements
    const testimonials = document.querySelectorAll('.testimonial');
    const prevBtn = document.querySelector('.testimonial-nav.prev');
    const nextBtn = document.querySelector('.testimonial-nav.next');
    const getStartedBtn = document.getElementById('getStartedBtn');
    let index = 0;

    // Show testimonial at given index
    function showTestimonial(i) {
        testimonials.forEach((t, idx) => {
            t.style.display = idx === i ? 'block' : 'none';
        });
    }

    // Initially show the first testimonial
    showTestimonial(index);

    // Previous button click
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            index = (index - 1 + testimonials.length) % testimonials.length;
            showTestimonial(index);
        });
    }

    // Next button click
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            index = (index + 1) % testimonials.length;
            showTestimonial(index);
        });
    }

    // Auto-slide every 6 seconds
    setInterval(() => {
        index = (index + 1) % testimonials.length;
        showTestimonial(index);
    }, 6000);

    // Redirect button logic
    if (getStartedBtn) {
        getStartedBtn.addEventListener('click', () => {
            const redirectUrl = getStartedBtn.getAttribute('data-url');
            if (redirectUrl) {
                window.location.href = redirectUrl;
            }
        });
    }
});
