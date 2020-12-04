document.addEventListener('DOMContentLoaded', function() {
  /**
   * show the page and all content on the page
   */
  editProfile();
  loadProfile();

  editTagline();
  loadTagline();
});

function loadProfile() {
  /**
   * load profile view
   */
  document.querySelector('#profile-view').style.display = 'block';
  document.querySelector('#edit-profile-view').style.display = 'none';
}

function loadEditProfileView() {
  /**
   * load edit profile view
   */
  document.querySelector('#profile-view').style.display = 'none';
  document.querySelector('#edit-profile-view').style.display = 'block';
}

function editProfile() {
  /**
   * assign edit profile listener to edit buttons on the page
   */
  document.querySelectorAll('.edit-profile').forEach(btn => {
    btn.addEventListener('click', function() {
      const profileId = btn.dataset.profile;

      loadEditProfileView();
      submitEditProfile(profileId);
    });
  });
}

function submitEditProfile(profileId) {
  /**
   * submit edit profile to backend
   */
  document.querySelector('#edit-profile-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const updatedProfile = document.querySelector('.edit-profile-field').value;
    putEditProfileFetch(profileId, updatedProfile);
  });
}

function putEditProfileFetch(userId, updatedProfile) {
  /**
   * post updated profile to the backend
   */
  const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  fetch(`/users/${userId}/edit`, {
    headers: {"X-CSRFToken": token },
    method: 'PUT',
    body: JSON.stringify({
      profile: updatedProfile
    })
  })
  .then(response => response.json())
  .then(data => {
    document.querySelector("#profile-content").innerHTML = data['profile'];
    loadProfile();
  })
  .catch()
}