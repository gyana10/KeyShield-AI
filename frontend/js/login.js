document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const alertBox = document.getElementById("alert-box");
    const submitBtn = document.getElementById("submit-btn");

    function showAlert(msg, isError = true) {
        alertBox.style.display = "block";
        alertBox.textContent = msg;
        alertBox.className = isError ? "badge badge-high" : "badge badge-low";
        alertBox.style.width = "100%";
    }

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        alertBox.style.display = "none";

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        if (!email || !password) {
            showAlert("Please fill in all fields.");
            return;
        }

        try {
            submitBtn.disabled = true;
            submitBtn.textContent = "Signing in...";

            await ApiClient.login(email, password);
            showAlert("Login successful! Redirecting...", false);

            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 800);
        } catch (err) {
            showAlert(err.message || "Invalid credentials.");
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = "Sign In";
        }
    });
});