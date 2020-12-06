document.addEventListener('DOMContentLoaded', function() {
  /**
   * show the page and all content on the page
   */
  
  // listen for the single instance where profile-view is on the page, then
  // listen for specific buttons to be pressed
  const profileViewExistsOnThisPage = document.getElementById("profile-view");
  if(profileViewExistsOnThisPage){
    editProfile();
    loadProfile();
  
    editTagline();
    loadTagline();
  }


  // listen for category dropdown to be pressed
  // normally I might use context to keep the categories 
  // so that I wouldn't have to reload them every time I 
  // check the categories button

});

function editProfilePage() {
  
  editProfile();
  loadProfile();

  editTagline();
  loadTagline();
}

/**
 * loading and hiding different parts of the 
 * thought to make this dynamic and then thought this may 
 * cause some confusion so I chose not to...
 * 
 * I originally made these two different files. As the 
 * project grows
 */
function loadProfile() {
  /**
   * load profile view
   */
  document.querySelector('#profile-view').style.display = 'block';
  document.querySelector('#edit-profile-view').style.display = 'none';
}

function loadTagline() {
  /**
   * load tagline view
   */
  document.querySelector('#tagline-view').style.display = 'block';
  document.querySelector('#edit-tagline-view').style.display = 'none';
}

function loadEditProfileView() {
  /**
   * load edit profile view
   */
  document.querySelector('#profile-view').style.display = 'none';
  document.querySelector('#edit-profile-view').style.display = 'block';
}

function loadEditTaglineView() {
  /**
   * load edit tagline view
   */
  document.querySelector('#tagline-view').style.display = 'none';
  document.querySelector('#edit-tagline-view').style.display = 'block';
}

/**
 * editing and submitting the next parts
 */
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

function editTagline() {
  /**
   * assign edit tagline listener to edit buttons on the page
   */
  document.querySelectorAll('.edit-tagline').forEach(btn => {
    btn.addEventListener('click', function() {
      const taglineId = btn.dataset.tagline;

      loadEditTaglineView();
      submitEditTagline(taglineId);
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

function submitEditTagline(taglineId) {
  /**
   * submit edit tagline to backend
   */
  document.querySelector('#edit-tagline-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const updatedTagline = document.querySelector('.edit-tagline-field').value;
    putEditTaglineFetch(taglineId, updatedTagline);
  });
}

/**
 * updating the backend
 */
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

function putEditTaglineFetch(userId, updatedTagline) {
  /**
   * post updated tagline to the backend
  */
  const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  fetch(`/users/${userId}/edit`, {
    headers: {"X-CSRFToken": token },
    method: 'PUT',
    body: JSON.stringify({
      tagline: updatedTagline
    })
  })
  .then(response => response.json())
  .then(data => {
    document.querySelector("#tagline-content").innerHTML = data['tagline'];
    loadTagline();
  })
  .catch()
}