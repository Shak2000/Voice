// Home page functionality
document.addEventListener('DOMContentLoaded', function() {
    // Load the navigation toolbar
    loadToolbar();
    
    // Add interactive animations
    initializeAnimations();
    
    // Handle game card interactions
    initializeGameCards();
});

function loadToolbar() {
    const toolbarContainer = document.getElementById('toolbar-container');
    if (toolbarContainer) {
        fetch('/static/index.html')
            .then(response => response.text())
            .then(html => {
                toolbarContainer.innerHTML = html;
                highlightCurrentPage();
            })
            .catch(error => {
                console.error('Error loading toolbar:', error);
            });
    }
}

function highlightCurrentPage() {
    // Highlight the current page in the toolbar
    const currentPath = window.location.pathname;
    const toolbarLinks = document.querySelectorAll('.toolbar-link');
    
    toolbarLinks.forEach(link => {
        const href = link.getAttribute('href');
        if ((currentPath === '/' && href === '/') || 
            (currentPath !== '/' && href === currentPath)) {
            link.classList.add('active');
        }
    });
}

function initializeAnimations() {
    // Add scroll-based animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    // Observe game cards and other elements
    const animatedElements = document.querySelectorAll('.game-card, .quick-access');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

function initializeGameCards() {
    const gameCards = document.querySelectorAll('.game-card');
    
    gameCards.forEach(card => {
        // Add hover effects
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        // Add click ripple effect
        card.addEventListener('click', function(e) {
            const ripple = document.createElement('div');
            ripple.classList.add('ripple');
            
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Add quick link interactions
    const quickLinks = document.querySelectorAll('.quick-link');
    quickLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.quick-icon');
            icon.style.transform = 'scale(1.2) rotate(5deg)';
        });
        
        link.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.quick-icon');
            icon.style.transform = 'scale(1) rotate(0deg)';
        });
    });
}

// Add a welcome message animation
function showWelcomeMessage() {
    const header = document.querySelector('.home-hero h1');
    if (header) {
        header.style.opacity = '0';
        header.style.transform = 'translateY(-20px)';
        
        setTimeout(() => {
            header.style.transition = 'opacity 1s ease, transform 1s ease';
            header.style.opacity = '1';
            header.style.transform = 'translateY(0)';
        }, 100);
    }
}

// Initialize welcome animation
showWelcomeMessage();
