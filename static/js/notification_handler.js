// Notification handler JavaScript

function setupNotifications() {
    // Toggle notifications when the bell icon is clicked
    document.getElementById('notificationBellBtn').addEventListener('click', function() {
        // Find and click the hidden button
        document.querySelector('[data-testid="stButton"] button').click();
    });
}

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    setupNotifications();
});