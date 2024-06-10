// script.js

const previousUrl = "{{ previous_url | default(url_for('index')) }}"; // Default to the root URL if previous_url is not provided

document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById("popup");
    const closeBtn = document.querySelector(".close-btn");

    // Functionality to close the popup and redirect to the previous page
    closeBtn.addEventListener("click", function () {
        window.location.href = previousUrl;
    });

    // Optionally, close the popup when clicking outside of it and redirect to the previous page
    document.addEventListener("click", function (event) {
        if (event.target === popup) {
            window.location.href = previousUrl;
        }
    });
});