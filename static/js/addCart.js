document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const ticketId = this.getAttribute('data-ticket-id');
            
            // Send AJAX request to add the ticket to the cart
            fetch(`/add_to_cart/${ticketId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Item added to cart!');
                    // Optionally update cart count or UI
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
