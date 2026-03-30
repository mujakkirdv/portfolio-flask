// static/js/main.js
// Counter Animation
document.addEventListener('DOMContentLoaded', function() {
    const counters = document.querySelectorAll('.counter');
    
    const animateCounter = (counter) => {
        const target = parseInt(counter.getAttribute('data-target'));
        let current = 0;
        const increment = target / 50;
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.ceil(current) + '+';
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target + '+';
            }
        };
        updateCounter();
    };
    
    // Check if element is in viewport
    const isInViewport = (element) => {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    };
    
    // Animate counters when they come into view
    const handleScroll = () => {
        counters.forEach(counter => {
            if (isInViewport(counter) && !counter.hasAnimated) {
                counter.hasAnimated = true;
                animateCounter(counter);
            }
        });
    };
    
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Check on load
    
    // Contact Form Submission
    const contactForm = document.getElementById('contactForm');
    const formMessage = document.getElementById('formMessage');
    
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
            submitBtn.disabled = true;
            
            const formData = new FormData(contactForm);
            
            try {
                const response = await fetch('/send_message', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    formMessage.innerHTML = '<div class="alert alert-success">Message sent successfully! I\'ll get back to you soon.</div>';
                    contactForm.reset();
                } else {
                    formMessage.innerHTML = '<div class="alert alert-danger">Something went wrong. Please try again.</div>';
                }
            } catch (error) {
                formMessage.innerHTML = '<div class="alert alert-danger">Network error. Please try again.</div>';
            } finally {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                
                // Clear message after 5 seconds
                setTimeout(() => {
                    formMessage.innerHTML = '';
                }, 5000);
            }
        });
    }
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add fade-in animation to elements
    const fadeElements = document.querySelectorAll('.stat-card, .project-card, .skill-category');
    
    const fadeInOnScroll = () => {
        fadeElements.forEach(element => {
            if (isInViewport(element) && !element.classList.contains('fade-in-up')) {
                element.classList.add('fade-in-up');
            }
        });
    };
    
    window.addEventListener('scroll', fadeInOnScroll);
    fadeInOnScroll();
});