/**
 * Silent Eye - Main JavaScript (Optimized)
 * Handles scrollspy, smooth scrolling, and interactive features
 */

document.addEventListener('DOMContentLoaded', function() {
    // 1. Initialize utilities (defined at the bottom)
    const THROTTLE_LIMIT = 16; // ~60 FPS

    // 2. Initialize core features
    initScrollSpy(THROTTLE_LIMIT);
    initSmoothScrolling();

    // 3. Initialize interactive features
    initScrollAnimations();
    initMobileMenuHandling();
    initHideOnScroll(THROTTLE_LIMIT);
    initContactForm();
});

// --- CORE FEATURE INITIALIZATION ---

/**
 * ScrollSpy - Highlights active navigation items based on scroll position
 */
function initScrollSpy(throttleLimit) {
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const sections = document.querySelectorAll('section[id]');
    const header = document.querySelector('.fixed-header-wrapper');
    const HEADER_OFFSET = header ? header.offsetHeight : 128; // Dynamic header height, fallback to 128

    if (navLinks.length === 0 || sections.length === 0) return;

    // Pre-map section IDs to their corresponding nav links for faster lookup
    const sectionLinkMap = new Map();
    sections.forEach(section => {
        const link = document.querySelector(`.navbar-nav .nav-link[href="#${section.id}"]`);
        if (link) {
            sectionLinkMap.set(section.id, link);
        }
    });

    function updateActiveNavLink() {
        const scrollY = window.pageYOffset || document.documentElement.scrollTop;
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;

        // 1. Remove active class from all links
        navLinks.forEach(link => link.classList.remove('active'));

        // 2. Check if we're near the bottom of the page (Last section logic)
        // Use a small buffer (e.g., 5px) to detect the very bottom
        if (Math.ceil(scrollY + windowHeight) >= documentHeight - 5) {
            const lastSection = sections[sections.length - 1];
            const lastLink = sectionLinkMap.get(lastSection.id);
            if (lastLink) lastLink.classList.add('active');
            return;
        }

        // 3. Find the current section (Iterate backwards for correct stacking/overlap)
        for (let i = sections.length - 1; i >= 0; i--) {
            const section = sections[i];
            // Adjust section top position by the header offset
            const sectionTop = section.offsetTop - HEADER_OFFSET; 
            const sectionBottom = sectionTop + section.offsetHeight;

            if (scrollY >= sectionTop && scrollY < sectionBottom) {
                const activeLink = sectionLinkMap.get(section.id);
                if (activeLink) activeLink.classList.add('active');
                break;
            }
        }
    }

    // Use the throttle utility for performance
    const throttledScroll = throttle(updateActiveNavLink, throttleLimit);

    // Initial check and scroll listener
    updateActiveNavLink();
    window.addEventListener('scroll', throttledScroll, { passive: true });
}

/**
 * Smooth Scrolling - Enhances anchor link navigation
 */
function initSmoothScrolling() {
    // Note: Relying on CSS scroll-behavior: smooth for most links.
    
    // Handle navbar brand click to scroll to top
    const navbarBrand = document.querySelector('.navbar-brand');
    if (navbarBrand) {
        navbarBrand.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#hero' || href === '#') {
                e.preventDefault();
                // Manually scroll to top for consistency and reliability
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }
        });
    }
}

// --- INTERACTIVE FEATURES ---

/**
 * Scroll Animations - Add fade-in effects to sections
 */
function initScrollAnimations() {
    const observerOptions = {
        // Reduced threshold for better perceived performance
        threshold: 0.05, 
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                // Optional: Stop observing after it has faded in once
                observer.unobserve(entry.target); 
            }
        });
    }, observerOptions);

    // Observe all sections
    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });
}

/**
 * Mobile Menu Handling - Close mobile menu when link is clicked
 */
function initMobileMenuHandling() {
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarContainer = document.querySelector('.navbar'); // Use container for click-outside

    if (!navbarCollapse || !navbarToggler) return;

    // Helper function to close the menu, ensuring ARIA state is updated
    function closeMobileMenu() {
        if (navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
            navbarToggler.classList.add('collapsed');
            navbarToggler.setAttribute('aria-expanded', 'false');
        }
    }

    // 1. Close menu on link click
    navLinks.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });

    // 2. Close menu when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInsideNav = navbarContainer.contains(event.target);
        
        if (!isClickInsideNav) {
            closeMobileMenu();
        }
    });

    // 3. Listen to toggler clicks to update ARIA state when opening (in case of manual DOM manipulation)
    navbarToggler.addEventListener('click', function() {
        if (navbarCollapse.classList.contains('show')) {
            navbarToggler.setAttribute('aria-expanded', 'false');
        } else {
            navbarToggler.setAttribute('aria-expanded', 'true');
        }
    });
}

/**
 * Hide Navbar on Scroll Down - Show on Scroll Up
 */
function initHideOnScroll(throttleLimit) {
    const navbar = document.querySelector('.navbar');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    if (!navbar) return;

    let lastScrollY = window.scrollY;
    let isHidden = false;

    // Only enable on larger screens (desktop/tablet)
    const mediaQuery = window.matchMedia('(min-width: 768px)');

    function handleScroll() {
        if (!mediaQuery.matches) return; // Disable on mobile

        // IMPORTANT: If the mobile menu is open, do not hide the navbar
        if (navbarCollapse && navbarCollapse.classList.contains('show')) {
             return;
         }

        const header = document.querySelector('.fixed-header-wrapper');
        const headerHeight = header ? header.offsetHeight : 128;
        const currentScrollY = window.scrollY;
        const scrollDelta = currentScrollY - lastScrollY;

        if (Math.abs(scrollDelta) < 10) return;

        if (scrollDelta > 0 && !isHidden && currentScrollY > headerHeight) {
            // Scrolling down - hide navbar
            navbar.classList.add('hide-on-scroll');
            isHidden = true;
        } else if (scrollDelta < 0 && isHidden) {
            // Scrolling up - show navbar
            navbar.classList.remove('hide-on-scroll');
            isHidden = false;
        }

        lastScrollY = currentScrollY;
    }

    // Use the throttle utility
    const throttledScroll = throttle(handleScroll, throttleLimit);

    // Listen for scroll events
    window.addEventListener('scroll', throttledScroll, { passive: true });

    // Listen for screen size changes
    mediaQuery.addEventListener('change', function(e) {
        if (!e.matches && isHidden) {
            // Show navbar on mobile
            navbar.classList.remove('hide-on-scroll');
            isHidden = false;
        }
    });
}

// --- CONTACT FORM FUNCTIONALITY ---

/**
 * Initialize contact form enhancements
 */
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnSpinner = document.getElementById('btnSpinner');
    
    if (!contactForm || !submitBtn) return;

    // Form validation and enhancement
    const inputs = contactForm.querySelectorAll('input, textarea, select');
    
    // Add real-time validation
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldErrors);
    });

    // Form submission handler
    contactForm.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            return;
        }

        // Show loading state
        setLoadingState(true);
    });

    function validateField(e) {
        const field = e.target;
        const value = field.value.trim();
        
        // Remove existing validation classes
        field.classList.remove('is-valid', 'is-invalid');
        
        if (field.hasAttribute('required') && !value) {
            field.classList.add('is-invalid');
            return false;
        }
        
        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                field.classList.add('is-invalid');
                return false;
            }
        }
        
        // Name validation
        if (field.name === 'name' && value && value.length < 2) {
            field.classList.add('is-invalid');
            return false;
        }
        
        // Message validation
        if (field.name === 'message' && value && value.length < 10) {
            field.classList.add('is-invalid');
            return false;
        }
        
        // If validation passes and field has content
        if (value) {
            field.classList.add('is-valid');
        }
        
        return true;
    }

    function clearFieldErrors(e) {
        const field = e.target;
        field.classList.remove('is-invalid');
    }

    function validateForm() {
        let isValid = true;
        inputs.forEach(input => {
            const event = { target: input };
            if (!validateField(event)) {
                isValid = false;
            }
        });
        return isValid;
    }

    function setLoadingState(loading) {
        if (loading) {
            submitBtn.disabled = true;
            btnText.textContent = 'Sending...';
            btnSpinner.style.display = 'inline-block';
        } else {
            submitBtn.disabled = false;
            btnText.textContent = 'Send Message';
            btnSpinner.style.display = 'none';
        }
    }
}

// --- UTILITY FUNCTIONS (Kept for external use) ---

/**
 * Throttle function for performance optimization
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}