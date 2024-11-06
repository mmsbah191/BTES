// delete-from-db button
document.querySelectorAll('.delete-from-db').forEach(button => {
    button.addEventListener('click', (event) => {
        const ticketId = event.target.dataset.ticketId;
        fetch(`/delete_event/${ticketId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        }).then(response => {
            if (response.ok) {
                // Refresh the page or remove the event from the DOM
                location.reload();
            } else {
                alert("Failed to delete event.");
            }
        });
    });
});

// edit-from-db button
document.querySelectorAll('.edit-from-db').forEach(button => {
    button.addEventListener('click', (event) => {
        const ticketId = event.target.dataset.ticketId;
        window.location.href = `/edit_event/${ticketId}/`; // Redirect to the edit page
    });
});

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
