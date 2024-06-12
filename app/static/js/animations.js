// animations.js

document.addEventListener("DOMContentLoaded", function() {
    const loadingScreen = document.getElementById('loading-screen');
    const topHalf = document.querySelector('.top-half');
    const bottomHalf = document.querySelector('.bottom-half');
    const loadingContent = document.querySelector('.loading-content');

    function transitionToMainContent() {
        // Add the fly-up animation to the loading content and top-half
        loadingContent.classList.add('fly-up');
        topHalf.classList.add('fly-up');

        // Add the fly-down animation to the bottom-half
        bottomHalf.classList.add('fly-down');

        // After the split screen effect, hide the loading screen and show the main content
        setTimeout(() => {
            loadingScreen.style.display = 'none';
        }, 1000); // Duration of the animations
    }

    // Add a click event listener to the loading screen
    loadingScreen.addEventListener('click', transitionToMainContent);

    // Automatically transition to the main content after 3 seconds
    setTimeout(transitionToMainContent, 1500);
});
