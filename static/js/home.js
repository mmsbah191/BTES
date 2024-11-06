document.addEventListener('DOMContentLoaded', function () {
    const profileToggle = document.getElementById('profile-toggle');
    const profileDropdown = document.getElementById('profile-dropdown');
  
    profileToggle.addEventListener('click', function (event) {
      event.preventDefault();
      profileDropdown.style.display = 
        profileDropdown.style.display === 'block' ? 'none' : 'block';
    });
  
    document.addEventListener('click', function (event) {
      if (!profileToggle.contains(event.target) && !profileDropdown.contains(event.target)) {
        profileDropdown.style.display = 'none';
      }
    });
  });
  