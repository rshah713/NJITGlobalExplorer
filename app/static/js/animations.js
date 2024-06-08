// animations.js

document.addEventListener("DOMContentLoaded", function() {
    const loadingScreen = document.getElementById('loading-screen');
    const mainContent = document.getElementById('main-content');

    // Add a click event listener to the loading screen
    loadingScreen.addEventListener('click', function() {
        // Hide the loading screen
        loadingScreen.style.display = 'none';

        // Show the main content
        mainContent.style.display = 'block';
    });
});
