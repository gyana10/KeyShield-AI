document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("register-form");
    const alertBox = document.getElementById("alert-box");
    const submitBtn = document.getElementById("submit-btn");

    function showAlert(msg, isError = true) {
        alertBox.style.display = "block";
        alertBox.textContent = msg;
        alertBox.className = isError ? "badge badge-high" : "badge badge-low";
        alertBox.style.width = "100%";
    }

    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        alertBox.style.display = "none";

        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        if (!username || !email || !password) {
            showAlert("Please fill in all fields.");
            return;
        }

        try {
            submitBtn.disabled = true;
            submitBtn.textContent = "Creating Account...";

            await ApiClient.register(username, email, password);
            showAlert("Registration Successful! Logging in...", false);

            // Automatically log in
            await ApiClient.login(email, password);
            setTimeout(() => {
                window.location.href = "enroll.html";
            }, 800);
        } catch (err) {
            showAlert(err.message || "Registration failed.");
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = "Create Account";
        }
    });
});