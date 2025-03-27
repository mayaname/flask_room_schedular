
// Password Show/Hide toggle button

document.getElementById('togglePassword').addEventListener('click', function() {
    const passwordField = document.getElementById('password');
    const showIcon = document.getElementById('showIcon');
    const hideIcon = document.getElementById('hideIcon');
    
    if (passwordField.type === 'password') {
      passwordField.type = 'text';
      showIcon.style.display = 'none';
      hideIcon.style.display = 'inline';
    } else {
      passwordField.type = 'password';
      showIcon.style.display = 'inline';
      hideIcon.style.display = 'none';
    }
  });