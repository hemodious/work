document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Send a POST request to the Flask backend
    
    const loginButton = document.getElementById('loginButton');
        const loadingOverlay = document.getElementById('loadingOverlay');

        loginButton.addEventListener('click', async () => {
            // Show loading spinner
            loadingOverlay.style.display = 'flex';

            try {
                // Simulate API login (replace with actual API call)
                await fakeApiCall();
                fetch('/login', {
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
                    window.location.href = data.redirectUrl;
                  
                       // Redirect to the URL returned by the server
                    
                })
                // Redirect to dashboard
              // Replace with your redirect URL
            } catch (error) {
                alert('Login failed! Please try again.');
            } finally {
                // Hide loading spinner after redirect or error
                loadingOverlay.style.display = 'none';
            }
        });

        // Simulate a fake API call for demonstration purposes
        async function fakeApiCall() {
            return new Promise((resolve) => setTimeout(resolve, 3000)); // Simulates a 3-second API call
        }

//Toggle passwor
        function togglePassword() {
            const passwordField = document.getElementById('password');
            const toggleIcon = document.getElementById('toggle-password');

            if (passwordField.type === 'password') {
                passwordField.type = 'text'; // Show password
                toggleIcon.classList.remove('fa-eye');
                toggleIcon.classList.add('fa-eye-slash'); // Change icon
            } else {
                passwordField.type = 'password'; // Hide password
                toggleIcon.classList.remove('fa-eye-slash');
                toggleIcon.classList.add('fa-eye'); // Change icon
            }
        }
    
});

//loading screen
