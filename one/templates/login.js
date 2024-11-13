document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/login', { // Update the URL to your API endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.text(); // Assuming the response is plain text
        document.getElementById('responseMessage').innerText = data;

        if (response.ok) {
            // Handle successful login, e.g., redirect to the dashboard
            window.location.href = 'http://127.0.0.1:5000/dashboard1'; // Update to your dashboard URL
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('responseMessage').innerText = 'An error occurred. Please try again.';
    }
});