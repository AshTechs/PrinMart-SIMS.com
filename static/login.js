document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent the form's default submission behavior

        // Collect form data
        const name = document.getElementById("name").value.trim();
        const password = document.getElementById("password").value.trim();

        // Validate input
        if (!name || !password) {
            alert("Please enter both admin name and password.");
            return;
        }

        try {
            // Send data to the backend as JSON
            const response = await fetch(form.action, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ name, password }),
            });

            const result = await response.json();

            if (response.ok) {
                // Handle successful login
                alert(result.message);
                if (result.redirect_url) {
                    window.location.href = result.redirect_url;
                }
            } else {
                // Handle login errors
                alert(result.error || "Login failed. Please try again.");
            }
        } catch (error) {
            console.error("Error during login:", error);
            alert("An error occurred while processing your request. Please try again later.");
        }
    });
});
