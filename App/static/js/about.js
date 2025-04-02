// Simple carousel functionality
document.addEventListener('DOMContentLoaded', function() {

    const prev = document.querySelector('.prev');
    const next = document.querySelector('.next');
    const testimonials = document.querySelectorAll('.testimonial');
    let currentIndex = 0;

    // Hide all testimonials except the first one
    testimonials.forEach((testimonial, index) => {
        if (index !== 0) {
            testimonial.style.display = 'none';
        }
    });

    prev.addEventListener('click', function() {
        testimonials[currentIndex].style.display = 'none';
        currentIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
        testimonials[currentIndex].style.display = 'block';
    });

    next.addEventListener('click', function() {
        testimonials[currentIndex].style.display = 'none';
        currentIndex = (currentIndex + 1) % testimonials.length;
        testimonials[currentIndex].style.display = 'block';
    });
});