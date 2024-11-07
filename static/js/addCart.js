document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // منع إرسال النموذج

            const ticketId = this.getAttribute('data-ticket-id');

            fetch(`/add_to_cart/${ticketId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Item added to cart!');
                    document.querySelector('#cart-count').textContent = data.cart_count;
                } else {
                    alert('Error adding item to cart.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});
