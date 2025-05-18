// Side menu for IFC viewer controls

// Create the side menu container
function createSideMenu() {
    const sideMenu = document.createElement('div');
    sideMenu.id = 'ifc-side-menu';
    sideMenu.style.position = 'absolute';
    sideMenu.style.top = '10px';
    sideMenu.style.right = '10px';
    sideMenu.style.zIndex = '100';
    sideMenu.style.display = 'flex';
    sideMenu.style.flexDirection = 'column';
    sideMenu.style.gap = '5px';
    
    document.getElementById('ifc-viewer-container').appendChild(sideMenu);
    return sideMenu;
}

// Get the side menu, creating it if needed
function getSideMenu() {
    let sideMenu = document.getElementById('ifc-side-menu');
    if (!sideMenu) {
        sideMenu = createSideMenu();
    }
    return sideMenu;
}

// Create a button for the side menu
function createSideMenuButton(icon, tooltip, onClick) {
    const sideMenu = getSideMenu();
    
    const button = document.createElement('button');
    button.className = 'side-menu-button';
    button.title = tooltip;
    button.style.width = '40px';
    button.style.height = '40px';
    button.style.borderRadius = '50%';
    button.style.border = 'none';
    button.style.backgroundColor = '#fff';
    button.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.2)';
    button.style.cursor = 'pointer';
    button.style.display = 'flex';
    button.style.alignItems = 'center';
    button.style.justifyContent = 'center';
    
    // Add icon
    if (icon) {
        const iconElement = document.createElement('span');
        iconElement.className = 'material-icons';
        iconElement.textContent = icon;
        button.appendChild(iconElement);
    }
    
    // Add click event
    if (onClick) {
        button.addEventListener('click', onClick);
    }
    
    sideMenu.appendChild(button);
    return button;
}

// Export functions
export { createSideMenuButton };