// Consolidated JavaScript for gcPanel
// This file combines functionality from various JS files

// ===== NOTIFICATION HANDLING =====
function setupNotifications() {
    // Toggle notifications when the bell icon is clicked
    const bellBtn = document.getElementById('notificationBellBtn');
    if (bellBtn) {
        bellBtn.addEventListener('click', function() {
            // Find and click the hidden button
            const hiddenBtn = document.querySelector('[data-testid="stButton"] button');
            if (hiddenBtn) hiddenBtn.click();
        });
    }
}

// ===== SIDEBAR HANDLING =====
function setupSidebar() {
    // Toggle sidebar visibility
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener('click', function() {
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                sidebar.classList.toggle('collapsed');
                // Update toggle button icon
                sidebarToggleBtn.innerHTML = sidebar.classList.contains('collapsed') 
                    ? '<span class="material-icons">menu</span>' 
                    : '<span class="material-icons">menu_open</span>';
            }
        });
    }
}

// ===== THEME SWITCHING =====
function setupThemeToggle() {
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function() {
            // This will trigger the hidden button that Streamlit uses for theme toggling
            const hiddenThemeBtn = document.querySelector('[data-testid="themeChangeBtn"] button');
            if (hiddenThemeBtn) hiddenThemeBtn.click();
            
            // Update the icon based on current theme
            const isDarkTheme = document.body.classList.contains('dark');
            themeToggleBtn.innerHTML = isDarkTheme 
                ? '<span class="material-icons">light_mode</span>' 
                : '<span class="material-icons">dark_mode</span>';
        });
    }
}

// ===== RESPONSIVE UI ADJUSTMENTS =====
function handleResponsiveLayout() {
    // Adjust layout for mobile screens
    function adjustForScreenSize() {
        const isMobile = window.innerWidth < 768;
        document.body.classList.toggle('mobile-view', isMobile);
        
        // Collapse sidebar on mobile by default
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar && isMobile) {
            sidebar.classList.add('collapsed');
        }
    }
    
    // Initial check
    adjustForScreenSize();
    
    // Listen for window resize
    window.addEventListener('resize', adjustForScreenSize);
}

// ===== USABILITY ENHANCEMENTS =====
function enhanceInputFields() {
    // Add clear button to text inputs
    document.querySelectorAll('input[type="text"]').forEach(input => {
        const clearBtn = document.createElement('button');
        clearBtn.className = 'input-clear-btn';
        clearBtn.innerHTML = '&times;';
        clearBtn.addEventListener('click', () => {
            input.value = '';
            input.dispatchEvent(new Event('input'));
            input.focus();
        });
        
        // Only show clear button when there's text
        input.addEventListener('input', () => {
            clearBtn.style.display = input.value ? 'block' : 'none';
        });
        
        // Initial state
        clearBtn.style.display = 'none';
        
        // Add clear button after input
        input.parentNode.style.position = 'relative';
        input.parentNode.appendChild(clearBtn);
    });
}

// ===== INITIALIZATION =====
// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    setupNotifications();
    setupSidebar();
    setupThemeToggle();
    handleResponsiveLayout();
    enhanceInputFields();
});

// Re-initialize when Streamlit app frame is re-rendered
// This is needed because Streamlit replaces DOM elements on updates
window.addEventListener('streamlit:render', function() {
    setupNotifications();
    setupSidebar();
    setupThemeToggle();
    enhanceInputFields();
});