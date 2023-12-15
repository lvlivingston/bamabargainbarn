cartItems = {{ cart_items|safe }};

console.log('Cart Items:', cartItems);


function removeItem(itemId) {
    const csrfToken = getCookie('csrftoken');
    console.log(`Removing item with ID: ${itemId}`);
    // Send a DELETE request to the server
    fetch(`/cart/delete/${itemId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken,  // Include CSRF token in the headers
            'Content-Type': 'application/json', // Specify content type
        },
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response
        console.log(data);

        // Check if the deletion was successful
        if (data.success) {
            // Optionally, you can redirect to the cart page
            // window.location.href = '/cart/';

            // Alternatively, you can reload the current page to refresh the cart view
            location.reload();
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function to get CSRF token from cookies
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Function to update quantity asynchronously
function updateQuantity(event, orderitem_id) {
    if (!orderitem_id) {
        console.error('Invalid OrderItem Id:', orderitem_id);
        return;
    }
    console.log(orderitem_id);
    console.log('Updating quantity for item:', orderitem_id);
    console.log('OrderItem Id:', orderitem_id);
    // Ensure that event is defined and is an event object
    if (event && event.preventDefault) {
        // Prevent the form from submitting in the traditional way
        event.preventDefault();

        // Get the selected quantity from the input field
        const selectedQuantity = document.getElementById(`quantity-${orderitem_id}`).value;

        const csrfToken = getCookie('csrftoken');
        console.log('CSRF Token:', csrfToken);

    // Send an AJAX request to update the quantity
    fetch(`/cart/update/${orderitem_id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
        },
    })

    .then(response => response.json())
    .then(data => {
        // Handle the response
        console.log('Response:', data);

        // Check if the update was successful
        if (data.success) {
            console.log('Update successful');
            // Reload the current page to refresh the cart view
            location.reload();
        }
    })
    .catch(error => console.error('Error:', error));
    }
}

// console.log('2nd Cart Items:', {{ cart_items|safe }});