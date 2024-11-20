document.getElementById('signup-button').addEventListener('click', async () => {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const repeatPassword = document.getElementById('repeat_password').value.trim();

    // Validate inputs
    if (!name || !email || !password || !repeatPassword) {
        alert('All fields are required!');
        return;
    }
    if (password !== repeatPassword) {
        alert('Passwords do not match!');
        return;
    }

    try {
        const response = await fetch('/admin/SuperAdsignup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, password, repeat_password: repeatPassword }),
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message); // "Super admin registered successfully!"

            // Redirect to verification page after successful registration
            window.location.href = `/admin/verification/${email}`;
        } else {
            alert(result.error); // Display the error message from the server
        }
    } catch (error) {
        alert('An error occurred while submitting the form. Please try again.');
        console.error(error);
    }
});
