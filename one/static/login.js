document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Send a POST request to the Flask backend
    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'email': email,
            'password': password
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Expecting a JSON response
    })
    .then(data => {
        console.log('Server response:', data.redirectUrl);
       
        // Check if redirectUrl is present in the response
      
            window.location.href = data.redirectUrl; // Redirect to the URL returned by the server
        
    })
    
    });
