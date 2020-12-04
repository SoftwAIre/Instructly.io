document.addEventListener('DOMContentLoaded', function() {
  /**
   * show the page and all content on the page
   */

  editTagline();
  loadTagline();
});

function loadTagline() {
  /**
   * load tagline view
   */
  document.querySelector('#tagline-view').style.display = 'block';
  document.querySelector('#edit-tagline-view').style.display = 'none';
}

function loadEditTaglineView() {
  /**
   * load edit tagline view
   */
  document.querySelector('#tagline-view').style.display = 'none';
  document.querySelector('#edit-tagline-view').style.display = 'block';
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