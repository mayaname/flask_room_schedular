// Function to hide the flash message after 5 seconds
function dismissFlashMessage() {
    setTimeout(function() {
        var flashMessage = document.getElementById('flash-message');
        if (flashMessage) {
            flashMessage.style.display = 'none';
        }
    }, 5000); // 5000 milliseconds = 5 seconds
}

// Call the function when the window loads
window.onload = dismissFlashMessage;