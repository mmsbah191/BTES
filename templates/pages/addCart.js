document.querySelector('#add-to-cart-btn').addEventListener('click', function() {
    let ticketId = this.getAttribute('data-ticket-id');
    
    fetch(`/add_to_cart/${ticketId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    }).then(response => response.json()).then(data => {
        if (data.success) {
            alert('تم إضافة التذكرة إلى السلة!');
            // تحديث عدد العناصر في السلة
            document.querySelector('#cart-count').textContent = data.cart_count;
        } else {
            alert('حدث خطأ في إضافة التذكرة.');
        }
    });
});
