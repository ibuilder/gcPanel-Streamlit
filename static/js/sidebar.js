// Sidebar Navigation JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
});

function initializeSidebar() {
    // Find all nav items
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        // Add click event listener
        item.addEventListener('click', function() {
            // Remove active class from all items
            navItems.forEach(i => i.classList.remove('active'));
            
            // Add active class to clicked item
            item.classList.add('active');
            
            // Find the associated streamlit button and click it
            const moduleName = item.getAttribute('data-module');
            if (moduleName) {
                const moduleButton = document.querySelector(`button[data-module="${moduleName}"]`);
                if (moduleButton) {
                    moduleButton.click();
                }
            }
        });
    });
    
    // Highlight the current active module
    highlightActiveModule();
}

function highlightActiveModule() {
    // Get current module from URL or session state
    const currentModule = getCurrentModule();
    
    if (currentModule) {
        // Find the nav item with matching data-module attribute
        const activeItem = document.querySelector(`.nav-item[data-module="${currentModule}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }
    }
}

function getCurrentModule() {
    // This is a placeholder - in a real app, you'd get this from URL params or session state
    // For now we'll just default to 'dashboard'
    return 'dashboard';
}