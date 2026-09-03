// Team 2 Lead Dashboard Enhancements
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize dashboard enhancements
    initDashboardEnhancements();
    
    // Initialize table enhancements
    initTableEnhancements();
    
    // Initialize card animations
    initCardAnimations();
});

function initDashboardEnhancements() {
    // Add smooth scrolling to anchor links
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
    
    // Add loading states to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('btn-expand')) {
                this.style.pointerEvents = 'none';
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.pointerEvents = 'auto';
                }, 2000);
            }
        });
    });
}

function initTableEnhancements() {
    // Add table row highlighting
    document.querySelectorAll('.data-table tbody tr').forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.001)';
            this.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = 'none';
        });
    });
    
    // Add table header sticky behavior
    const tables = document.querySelectorAll('.table-responsive');
    tables.forEach(table => {
        const thead = table.querySelector('thead');
        if (thead) {
            const observer = new IntersectionObserver(
                ([e]) => {
                    if (e.intersectionRatio < 1) {
                        thead.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
                    } else {
                        thead.style.boxShadow = 'none';
                    }
                },
                { threshold: [1] }
            );
            observer.observe(thead);
        }
    });
}

function initCardAnimations() {
    // Add intersection observer for card animations
    const cards = document.querySelectorAll('.data-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// Enhanced fullscreen functionality
function toggleFullscreen(button) {
    const card = button.closest('.data-card');
    const isFullscreen = card.classList.contains('fullscreen');
    
    if (isFullscreen) {
        // Exit fullscreen
        card.classList.remove('fullscreen');
        card.style.position = '';
        card.style.top = '';
        card.style.left = '';
        card.style.width = '';
        card.style.height = '';
        card.style.zIndex = '';
        card.style.margin = '';
        card.style.borderRadius = '';
        button.innerHTML = '<i class="fas fa-expand"></i>';
        
        // Scroll back to original position
        card.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
        // Enter fullscreen
        card.classList.add('fullscreen');
        card.style.position = 'fixed';
        card.style.top = '0';
        card.style.left = '0';
        card.style.width = '100vw';
        card.style.height = '100vh';
        card.style.zIndex = '1000';
        card.style.margin = '0';
        card.style.borderRadius = '0';
        button.innerHTML = '<i class="fas fa-compress"></i>';
        
        // Add escape key listener
        const escapeHandler = (e) => {
            if (e.key === 'Escape') {
                toggleFullscreen(button);
                document.removeEventListener('keydown', escapeHandler);
            }
        };
        document.addEventListener('keydown', escapeHandler);
    }
}

// Enhanced loading function
function showLoading() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
        loadingOverlay.style.opacity = '1';
        
        // Add a timeout to prevent infinite loading
        setTimeout(() => {
            if (loadingOverlay.style.display === 'flex') {
                loadingOverlay.style.opacity = '0';
                setTimeout(() => {
                    loadingOverlay.style.display = 'none';
                }, 300);
            }
        }, 10000); // 10 second timeout
    }
}

// Add keyboard navigation support
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + F to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        const dateInput = document.querySelector('input[type="date"]');
        if (dateInput) {
            dateInput.focus();
        }
    }
    
    // Escape to close fullscreen cards
    if (e.key === 'Escape') {
        const fullscreenCard = document.querySelector('.data-card.fullscreen');
        if (fullscreenCard) {
            const expandButton = fullscreenCard.querySelector('.btn-expand');
            if (expandButton) {
                toggleFullscreen(expandButton);
            }
        }
    }
});

// Create Action Popup functionality
function initCreateActionPopup() {
    const createActionBtns = document.querySelectorAll('.btn-create-action');
    const modal = document.getElementById('createActionModal');
    const closeBtn = document.querySelector('.modal-close-btn');
    const cancelBtn = document.querySelector('.btn-cancel-custom');
    const form = document.getElementById('createActionForm');
    
    if (!modal) return;
    
    // Open modal when create action button is clicked
    createActionBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Get the card title to pre-populate the form
            const card = this.closest('.data-card');
            const cardTitle = card.querySelector('.card-header h3').textContent.trim();
            const titleSelect = document.getElementById('modalTitleSelect');
            
            if (titleSelect) {
                // Try to find matching option
                const matchingOption = Array.from(titleSelect.options).find(option => 
                    option.textContent.includes(cardTitle) || cardTitle.includes(option.textContent.trim())
                );
                
                if (matchingOption) {
                    titleSelect.value = matchingOption.value;
                } else {
                    // Set custom title
                    const titleInputVisible = document.getElementById('modalTitleInputVisible');
                    const titleInput = document.getElementById('modalTitleInput');
                    if (titleInputVisible && titleInput) {
                        titleInputVisible.value = cardTitle;
                        titleInput.value = cardTitle;
                        titleInputVisible.style.display = 'block';
                        titleSelect.value = '';
                    }
                }
            }
            
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });
    
    // Close modal functions
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        form.reset();
        
        // Hide custom title input
        const titleInputVisible = document.getElementById('modalTitleInputVisible');
        const titleInput = document.getElementById('modalTitleInput');
        if (titleInputVisible) {
            titleInputVisible.style.display = 'none';
            titleInputVisible.value = '';
        }
        if (titleInput) {
            titleInput.value = '';
        }
    }
    
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', closeModal);
    }
    
    // Close modal when clicking outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
    
    // Handle form submission
    if (form) {
        form.addEventListener('submit', function(e) {
            // Show loading state
            const submitBtn = form.querySelector('.btn-submit-custom');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating...';
            submitBtn.disabled = true;
            
            // Ensure the title field is properly set
            const titleSelect = document.getElementById('modalTitleSelect');
            const titleInput = document.getElementById('modalTitleInput');
            const titleInputVisible = document.getElementById('modalTitleInputVisible');
            
            if (titleSelect && titleInput) {
                if (titleSelect.value) {
                    // Use selected value
                    titleInput.value = titleSelect.value;
                } else if (titleInputVisible && titleInputVisible.value) {
                    // Use custom title
                    titleInput.value = titleInputVisible.value;
                } else {
                    // No title selected or entered
                    e.preventDefault();
                    alert('Please select or enter a title for the action.');
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                    return;
                }
            }
            
            // Validate other required fields
            const assignedUser = document.getElementById('modalAssignedUser');
            const priority = document.getElementById('modalPriority');
            const dueDate = document.getElementById('modalDueDate');
            const action = document.getElementById('modalAction');
            
            if (!assignedUser.value) {
                e.preventDefault();
                alert('Please select a user to assign the action to.');
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                return;
            }
            
            if (!dueDate.value) {
                e.preventDefault();
                alert('Please select a due date for the action.');
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                return;
            }
            
            if (!action.value.trim()) {
                e.preventDefault();
                alert('Please enter action details.');
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                return;
            }
            
            // Allow the form to submit normally
            // The form will submit to the server and redirect back
        });
    }
    
    // Handle title select changes
    const titleSelect = document.getElementById('modalTitleSelect');
    const titleInput = document.getElementById('modalTitleInput');
    const titleInputVisible = document.getElementById('modalTitleInputVisible');
    
    if (titleSelect && titleInput && titleInputVisible) {
        titleSelect.addEventListener('change', function() {
            if (this.value === '') {
                titleInputVisible.style.display = 'block';
                titleInputVisible.required = true;
                titleInputVisible.value = '';
                titleInput.value = '';
            } else {
                titleInputVisible.style.display = 'none';
                titleInputVisible.required = false;
                titleInput.value = this.value;
            }
        });
        
        // Also handle changes to the visible input
        titleInputVisible.addEventListener('input', function() {
            titleInput.value = this.value;
        });
    }
    
    // Set default due date to tomorrow
    const dueDateInput = document.getElementById('modalDueDate');
    if (dueDateInput) {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        tomorrow.setHours(17, 0); // Set to 5 PM
        dueDateInput.value = tomorrow.toISOString().slice(0, 16);
    }
}

// Quick Navigation functionality
function initQuickNavigation() {
    const navBtn = document.getElementById('quickNavBtn');
    const navContent = document.getElementById('quickNavContent');
    
    if (!navBtn || !navContent) return;
    
    // Toggle dropdown
    navBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const isActive = navContent.classList.contains('active');
        
        if (isActive) {
            navContent.classList.remove('active');
            navBtn.classList.remove('active');
        } else {
            navContent.classList.add('active');
            navBtn.classList.add('active');
        }
    });
    
    // Prevent global loader from interfering with dropdown
    navContent.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!navBtn.contains(e.target) && !navContent.contains(e.target)) {
            navContent.classList.remove('active');
            navBtn.classList.remove('active');
        }
    });
    
    // Close dropdown on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navContent.classList.contains('active')) {
            navContent.classList.remove('active');
            navBtn.classList.remove('active');
        }
    });
    
    // Handle navigation item clicks
    const navItems = navContent.querySelectorAll('.nav-dropdown-item');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                // Prevent global loader from showing during smooth scroll
                const globalLoader = document.getElementById('global-loader');
                if (globalLoader) {
                    globalLoader.style.pointerEvents = 'none';
                }
                
                // Smooth scroll to target
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Close dropdown
                navContent.classList.remove('active');
                navBtn.classList.remove('active');
                
                // Update current selection
                navItems.forEach(navItem => navItem.classList.remove('current'));
                this.classList.add('current');
                
                // Update button text
                const btnText = navBtn.querySelector('.nav-btn-text');
                if (btnText) {
                    btnText.textContent = this.textContent.trim();
                }
                
                // Add highlight effect to target card
                targetElement.style.transform = 'scale(1.02)';
                targetElement.style.boxShadow = '0 8px 32px rgba(44, 62, 80, 0.2)';
                
                // Wait for scroll animation to complete, then restore global loader
                setTimeout(() => {
                    targetElement.style.transform = '';
                    targetElement.style.boxShadow = '';
                    
                    // Ensure global loader is hidden after scroll animation
                    if (globalLoader) {
                        globalLoader.classList.add('hide');
                        globalLoader.style.pointerEvents = '';
                    }
                }, 1000);
            }
        });
    });
    
    // Update current section based on scroll position
    function updateCurrentSection() {
        const cards = document.querySelectorAll('.data-card');
        const scrollPosition = window.scrollY + 100; // Offset for header
        
        let currentCard = null;
        cards.forEach(card => {
            const cardTop = card.offsetTop;
            const cardBottom = cardTop + card.offsetHeight;
            
            if (scrollPosition >= cardTop && scrollPosition < cardBottom) {
                currentCard = card;
            }
        });
        
        if (currentCard) {
            const cardId = currentCard.id;
            navItems.forEach(navItem => {
                navItem.classList.remove('current');
                if (navItem.getAttribute('data-target') === cardId) {
                    navItem.classList.add('current');
                    
                    // Update button text
                    const btnText = navBtn.querySelector('.nav-btn-text');
                    if (btnText) {
                        btnText.textContent = navItem.textContent.trim();
                    }
                }
            });
        }
    }
    
    // Throttled scroll listener
    let scrollTimeout;
    window.addEventListener('scroll', function() {
        if (scrollTimeout) {
            clearTimeout(scrollTimeout);
        }
        scrollTimeout = setTimeout(updateCurrentSection, 100);
    });
    
    // Initialize current section
    updateCurrentSection();
}

// Add performance monitoring
window.addEventListener('load', function() {
    // Log page load performance
    if ('performance' in window) {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log(`Dashboard loaded in ${loadTime}ms`);
    }
    
    // Initialize create action popup
    initCreateActionPopup();
    
    // Initialize quick navigation
    initQuickNavigation();
}); 