// ============ Custom Dialog Popup ====================================

document.getElementById("delete-link").onclick = function(event) {
    event.preventDefault(); // Prevent the default action
    document.getElementById("confirm-dialog").style.display = "block"; // Show the custom dialog
};
  
document.getElementById("confirm-yes-button").onclick = function() {
const deleteUrl = this.getAttribute('data-url');
window.location.href = deleteUrl;
};

function closeDialog() {
document.getElementById("confirm-dialog").style.display = "none"; // Hide the custom dialog
}
  