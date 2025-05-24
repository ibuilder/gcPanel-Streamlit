"""
Enhanced JavaScript Interactions for Highland Tower Development Dashboard

This module provides smooth animations, interactive elements, and improved
user experience specifically designed for construction project management.
"""

import streamlit as st

def add_construction_dashboard_js():
    """Add enhanced JavaScript functionality for construction dashboard"""
    
    st.markdown("""
    <script>
    // Construction Dashboard Enhanced Interactions
    class ConstructionDashboard {
        constructor() {
            this.init();
        }
        
        init() {
            this.addSmoothScrolling();
            this.addCardAnimations();
            this.addProgressAnimations();
            this.addTooltips();
            this.addKeyboardShortcuts();
            this.addLoadingStates();
        }
        
        // Smooth scrolling for navigation
        addSmoothScrolling() {
            document.documentElement.style.scrollBehavior = 'smooth';
        }
        
        // Animated card hover effects
        addCardAnimations() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }
                });
            }, { threshold: 0.1 });
            
            // Observe cards when they're added to DOM
            const checkForCards = () => {
                document.querySelectorAll('.module-card, .metric-card').forEach(card => {
                    if (!card.dataset.animated) {
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(20px)';
                        card.style.transition = 'all 0.6s ease';
                        observer.observe(card);
                        card.dataset.animated = 'true';
                    }
                });
            };
            
            // Check for cards periodically
            setInterval(checkForCards, 500);
            checkForCards();
        }
        
        // Animated progress bars
        addProgressAnimations() {
            const animateProgress = () => {
                document.querySelectorAll('.progress-fill').forEach(bar => {
                    if (!bar.dataset.animated) {
                        const width = bar.style.width;
                        bar.style.width = '0%';
                        setTimeout(() => {
                            bar.style.width = width;
                        }, 300);
                        bar.dataset.animated = 'true';
                    }
                });
            };
            
            // Animate progress bars when they appear
            const progressObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateProgress();
                    }
                });
            });
            
            setInterval(() => {
                document.querySelectorAll('.progress-container').forEach(container => {
                    progressObserver.observe(container);
                });
            }, 500);
        }
        
        // Enhanced tooltips
        addTooltips() {
            document.addEventListener('mouseover', (e) => {
                if (e.target.hasAttribute('title') || e.target.closest('[title]')) {
                    const element = e.target.hasAttribute('title') ? e.target : e.target.closest('[title]');
                    const title = element.getAttribute('title');
                    
                    if (title && !element.dataset.tooltipAdded) {
                        element.dataset.tooltipAdded = 'true';
                        element.style.position = 'relative';
                        
                        const tooltip = document.createElement('div');
                        tooltip.innerHTML = title;
                        tooltip.style.cssText = `
                            position: absolute;
                            bottom: 100%;
                            left: 50%;
                            transform: translateX(-50%);
                            background: #1e293b;
                            color: white;
                            padding: 8px 12px;
                            border-radius: 6px;
                            font-size: 12px;
                            white-space: nowrap;
                            z-index: 1000;
                            opacity: 0;
                            transition: opacity 0.3s ease;
                            pointer-events: none;
                        `;
                        
                        element.appendChild(tooltip);
                        
                        element.addEventListener('mouseenter', () => {
                            tooltip.style.opacity = '1';
                        });
                        
                        element.addEventListener('mouseleave', () => {
                            tooltip.style.opacity = '0';
                        });
                    }
                }
            });
        }
        
        // Keyboard shortcuts for construction dashboard
        addKeyboardShortcuts() {
            document.addEventListener('keydown', (e) => {
                // Alt + D for Dashboard
                if (e.altKey && e.key === 'd') {
                    e.preventDefault();
                    this.navigateToModule('Dashboard');
                }
                
                // Alt + R for RFIs
                if (e.altKey && e.key === 'r') {
                    e.preventDefault();
                    this.navigateToModule('RFIs');
                }
                
                // Alt + S for Submittals
                if (e.altKey && e.key === 's') {
                    e.preventDefault();
                    this.navigateToModule('Submittals');
                }
                
                // Alt + T for Transmittals
                if (e.altKey && e.key === 't') {
                    e.preventDefault();
                    this.navigateToModule('Transmittals');
                }
                
                // Esc to close any modals or overlays
                if (e.key === 'Escape') {
                    document.querySelectorAll('.modal, .overlay').forEach(modal => {
                        modal.style.display = 'none';
                    });
                }
            });
        }
        
        // Navigate to module programmatically
        navigateToModule(moduleName) {
            const dropdown = document.querySelector('[data-testid="stSelectbox"] select');
            if (dropdown) {
                const options = Array.from(dropdown.options);
                const targetOption = options.find(option => 
                    option.text.includes(moduleName)
                );
                
                if (targetOption) {
                    dropdown.value = targetOption.value;
                    dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
        }
        
        // Loading states for buttons
        addLoadingStates() {
            document.addEventListener('click', (e) => {
                if (e.target.tagName === 'BUTTON' && !e.target.dataset.loading) {
                    e.target.dataset.loading = 'true';
                    const originalText = e.target.innerText;
                    
                    // Add loading spinner
                    e.target.innerHTML = `
                        <div style="display: flex; align-items: center; justify-content: center;">
                            <div class="loading-spinner" style="margin-right: 8px;"></div>
                            Processing...
                        </div>
                    `;
                    
                    // Reset after 2 seconds (Streamlit usually reloads by then)
                    setTimeout(() => {
                        e.target.innerHTML = originalText;
                        e.target.dataset.loading = 'false';
                    }, 2000);
                }
            });
        }
        
        // Auto-refresh for real-time data (construction sites need live updates)
        startAutoRefresh(intervalMinutes = 5) {
            setInterval(() => {
                // Only refresh if user is active
                if (document.hasFocus()) {
                    const refreshButton = document.querySelector('[aria-label="Refresh"]');
                    if (refreshButton) {
                        refreshButton.click();
                    }
                }
            }, intervalMinutes * 60 * 1000);
        }
        
        // Add construction-specific notifications
        showConstructionNotification(message, type = 'info', duration = 5000) {
            const notification = document.createElement('div');
            const icons = {
                'success': '✅',
                'warning': '⚠️',
                'error': '❌',
                'info': 'ℹ️'
            };
            
            notification.innerHTML = `
                <div style="
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: white;
                    border-left: 4px solid ${type === 'success' ? '#10b981' : type === 'warning' ? '#f59e0b' : type === 'error' ? '#ef4444' : '#3b82f6'};
                    padding: 1rem;
                    border-radius: 8px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                    z-index: 10000;
                    max-width: 300px;
                    transform: translateX(100%);
                    transition: transform 0.3s ease;
                ">
                    <div style="display: flex; align-items: center;">
                        <span style="margin-right: 8px; font-size: 1.2rem;">${icons[type]}</span>
                        <span style="font-weight: 500;">${message}</span>
                    </div>
                </div>
            `;
            
            document.body.appendChild(notification);
            
            // Animate in
            setTimeout(() => {
                notification.firstElementChild.style.transform = 'translateX(0)';
            }, 100);
            
            // Animate out and remove
            setTimeout(() => {
                notification.firstElementChild.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    document.body.removeChild(notification);
                }, 300);
            }, duration);
        }
    }
    
    // Initialize the construction dashboard when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.constructionDashboard = new ConstructionDashboard();
        });
    } else {
        window.constructionDashboard = new ConstructionDashboard();
    }
    
    // Keyboard shortcuts help overlay
    window.showKeyboardShortcuts = function() {
        const overlay = document.createElement('div');
        overlay.innerHTML = `
            <div style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                z-index: 20000;
                display: flex;
                align-items: center;
                justify-content: center;
            " onclick="this.remove()">
                <div style="
                    background: white;
                    padding: 2rem;
                    border-radius: 12px;
                    max-width: 400px;
                    width: 90%;
                ">
                    <h3 style="margin: 0 0 1rem 0; color: #1e293b;">⌨️ Keyboard Shortcuts</h3>
                    <div style="color: #64748b; line-height: 1.8;">
                        <div><kbd>Alt + D</kbd> → Dashboard</div>
                        <div><kbd>Alt + R</kbd> → RFIs</div>
                        <div><kbd>Alt + S</kbd> → Submittals</div>
                        <div><kbd>Alt + T</kbd> → Transmittals</div>
                        <div><kbd>Esc</kbd> → Close overlays</div>
                    </div>
                    <div style="margin-top: 1rem; text-align: center;">
                        <small style="color: #94a3b8;">Click anywhere to close</small>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
    };
    </script>
    """, unsafe_allow_html=True)

def add_construction_help_button():
    """Add a help button for keyboard shortcuts"""
    
    st.markdown("""
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
        <button onclick="showKeyboardShortcuts()" style="
            background: #3b82f6;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 1.2rem;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            transition: all 0.3s ease;
        " onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
            ?
        </button>
    </div>
    """, unsafe_allow_html=True)