/**
 * GitHub Repo Analyzer - Interactive Features
 * Enhances user experience with smooth animations and interactions
 */

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeFormHandling();
    initializeScrollAnimations();
    initializeInteractiveElements();
    initializeParticleEffect();
    addConsoleEasterEgg();
});

/**
 * Form handling with loading states
 */
function initializeFormHandling() {
    const form = document.getElementById('analyzeForm');
    const btn = document.getElementById('analyzeBtn');
    const input = document.getElementById('repo_url');
    
    if (!form || !btn) return;
    
    // Form submission
    form.addEventListener('submit', function(e) {
        // Validate URL
        const url = input.value.trim();
        if (!url.includes('github.com')) {
            e.preventDefault();
            showNotification('Please enter a valid GitHub repository URL', 'error');
            return;
        }
        
        // Add loading state
        btn.classList.add('loading');
btn.innerHTML = '<span style="opacity: 0;">🔍</span> Analyzing...';
btn.disabled = true;
// input.disabled = true;   // ❌ DO NOT disable input

        
        // Show loading animation
        showLoadingOverlay();
    });
    
    // Input validation on blur
    input.addEventListener('blur', function() {
        const url = this.value.trim();
        if (url && !url.includes('github.com')) {
            this.style.borderColor = 'var(--color-danger)';
            showNotification('URL must be a GitHub repository', 'warning');
        } else {
            this.style.borderColor = '';
        }
    });
    
    // Clear error on focus
    input.addEventListener('focus', function() {
        this.style.borderColor = '';
    });
}

/**
 * Scroll-based animations
 */
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0) scale(1)';
                entry.target.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                
                // Stagger animations for child elements with premium easing
                const children = entry.target.querySelectorAll('.stat-item, .tech-item, li');
                children.forEach((child, index) => {
                    child.style.opacity = '0';
                    child.style.transform = 'translateY(20px) scale(0.95)';
                    setTimeout(() => {
                        child.style.opacity = '1';
                        child.style.transform = 'translateY(0) scale(1)';
                        child.style.transition = 'all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
                    }, index * 60);
                });
                
                // Animate images with scale effect
                const images = entry.target.querySelectorAll('img');
                images.forEach((img, index) => {
                    img.style.opacity = '0';
                    img.style.transform = 'scale(0.9)';
                    setTimeout(() => {
                        img.style.opacity = '1';
                        img.style.transform = 'scale(1)';
                        img.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
                    }, index * 100 + 200);
                });
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });
}

/**
 * Interactive element enhancements
 */
function initializeInteractiveElements() {
    // Repository title click-to-copy
    const repoTitle = document.querySelector('.repo-title h3');
    if (repoTitle) {
        repoTitle.style.cursor = 'pointer';
        repoTitle.title = 'Click to copy repository name';
        
        repoTitle.addEventListener('click', function() {
            const text = this.textContent;
            copyToClipboard(text);
            
            const originalText = this.textContent;
            this.textContent = '✓ Copied!';
            this.style.color = 'var(--color-success)';
            
            setTimeout(() => {
                this.textContent = originalText;
                this.style.color = '';
            }, 1500);
        });
    }
    
    // Stat items hover effects with premium animation
    document.querySelectorAll('.stat-item').forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-6px) scale(1.04)';
            this.style.transition = 'all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });
    
    // Tech items premium animation on hover
    document.querySelectorAll('.tech-item').forEach(item => {
        item.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.tech-icon');
            if (icon) {
                icon.style.animation = 'float 1s ease-in-out infinite';
                icon.style.transform = 'scale(1.2) rotate(5deg)';
            }
        });
        
        item.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.tech-icon');
            if (icon) {
                icon.style.animation = '';
                icon.style.transform = 'scale(1) rotate(0deg)';
                icon.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            }
        });
    });
    
    // Badge premium hover effects
    document.querySelectorAll('.badge').forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.15) rotate(2deg)';
            this.style.transition = 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
            this.style.boxShadow = '0 4px 12px rgba(79, 156, 249, 0.4)';
        });
        
        badge.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            this.style.boxShadow = '';
        });
    });
    
    // Add premium animation to cards on scroll
    const cardObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0) scale(1)';
                entry.target.style.filter = 'blur(0px)';
            } else {
                entry.target.style.opacity = '0.3';
                entry.target.style.transform = 'translateY(20px) scale(0.98)';
                entry.target.style.filter = 'blur(2px)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    });
    
    document.querySelectorAll('.card').forEach(card => {
        card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        cardObserver.observe(card);
    });
}

/**
 * Subtle particle effect following mouse
 */
function initializeParticleEffect() {
    let mouseX = 0, mouseY = 0;
    let particles = [];
    
    document.addEventListener('mousemove', function(e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
        
        // Create particle occasionally
        if (Math.random() > 0.95) {
            createParticle(mouseX, mouseY);
        }
    });
    
    function createParticle(x, y) {
        const particle = document.createElement('div');
        particle.style.position = 'fixed';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.width = '4px';
        particle.style.height = '4px';
        particle.style.borderRadius = '50%';
        particle.style.background = 'var(--color-primary)';
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '9999';
        particle.style.opacity = '0.6';
        particle.style.transition = 'all 1s ease-out';
        
        document.body.appendChild(particle);
        
        // Animate particle
        setTimeout(() => {
            particle.style.transform = `translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) scale(0)`;
            particle.style.opacity = '0';
        }, 10);
        
        // Remove particle
        setTimeout(() => {
            particle.remove();
        }, 1000);
    }
}

/**
 * Loading overlay
 */
function showLoadingOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(10, 14, 26, 0.9);
        backdrop-filter: blur(10px);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease;
    `;
    
    overlay.innerHTML = `
        <div class="spinner"></div>
        <p class="loading-text" style="margin-top: 20px; font-size: 1.2rem; color: var(--color-text-secondary);">
            Analyzing repository...
        </p>
        <p style="margin-top: 10px; font-size: 0.9rem; color: var(--color-text-tertiary);">
            This may take a few moments
        </p>
    `;
    
    document.body.appendChild(overlay);
}

/**
 * Notification system
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: var(--color-bg-card);
        border: 1px solid ${type === 'error' ? 'var(--color-danger)' : type === 'warning' ? 'var(--color-warning)' : 'var(--color-primary)'};
        border-radius: var(--radius-md);
        color: var(--color-text-primary);
        box-shadow: var(--shadow-lg);
        z-index: 10001;
        animation: slideInRight 0.3s ease;
        backdrop-filter: blur(10px);
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Copy to clipboard utility
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success');
        }).catch(() => {
            fallbackCopy(text);
        });
    } else {
        fallbackCopy(text);
    }
}

function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    showNotification('Copied to clipboard!', 'success');
}

/**
 * Console easter egg
 */
function addConsoleEasterEgg() {
    const styles = [
        'font-size: 24px',
        'font-weight: bold',
        'background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
        '-webkit-background-clip: text',
        '-webkit-text-fill-color: transparent',
        'padding: 10px'
    ].join(';');
    
    console.log('%c⚡ GitHub Repo Analyzer', styles);
    console.log('%cBuilt with Flask ⚡', 'font-size: 14px; color: #60a5fa;');
    console.log('%cLooking for something? Check out the source code!', 'font-size: 12px; color: #94a3b8;');
}

/**
 * Add animation keyframes dynamically
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Smooth scroll behavior with premium easing
document.documentElement.style.scrollBehavior = 'smooth';
document.documentElement.style.scrollPaddingTop = '20px';

// Premium page load animation
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
        
        // Animate all cards with staggered entrance
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px) scale(0.95)';
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0) scale(1)';
                card.style.transition = 'all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)';
            }, index * 100 + 200);
        });
    }, 50);
});

// Performance optimization: Reduce animations on low-end devices
if (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) {
    document.body.classList.add('reduce-motion');
}

// Premium smooth scrolling for anchor links
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
