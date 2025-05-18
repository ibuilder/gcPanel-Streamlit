// Notification System JavaScript Functions

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeNotificationSystem();
});

function initializeNotificationSystem() {
    // Find the notification button
    const notificationBtn = document.getElementById('notification-btn');
    
    if (notificationBtn) {
        // Add click event listener
        notificationBtn.addEventListener('click', function() {
            // Find the hidden Streamlit button and click it
            const streamlitBtn = document.querySelector('[data-testid="stButton"] button');
            if (streamlitBtn) {
                streamlitBtn.click();
            }
        });
    }
    
    // Add animation effects to notification items
    animateNotificationItems();
}

function animateNotificationItems() {
    // Add animation effects to notification items
    const notificationItems = document.querySelectorAll('.notification-item');
    
    notificationItems.forEach((item, index) => {
        // Add a slight delay to each item for a cascading effect
        item.style.animationDelay = `${index * 0.05}s`;
        item.classList.add('animated-item');
    });
}

// Function to mark notification as read
function markAsRead(notificationId) {
    // This would typically send a request to the server
    console.log(`Marking notification ${notificationId} as read`);
    
    // Find the corresponding Streamlit button and click it
    const readButton = document.querySelector(`button[data-notification-id="${notificationId}"]`);
    if (readButton) {
        readButton.click();
    }
}

// Function to update notification badge count
function updateNotificationBadge(count) {
    const badge = document.querySelector('.notification-badge');
    
    if (badge) {
        if (count > 0) {
            badge.textContent = count;
            badge.style.display = 'flex';
        } else {
            badge.style.display = 'none';
        }
    }
}