const API_URL = "http://127.0.0.1:8000";

document
.getElementById("loginForm")
.addEventListener("submit", async function (e) {

    e.preventDefault();

    const data = {

        email: document.getElementById("email").value,

        password: document.getElementById("password").value

    };

    try {

        const response = await fetch(

            API_URL + "/login",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify(data)

            }

        );

        const result = await response.json();

        const message = document.getElementById("message");

        if (response.ok) {

            // Save JWT Token
            localStorage.setItem(
                "token",
                result.access_token
            );

            // Save Email (useful later)
            localStorage.setItem(
                "email",
                data.email
            );

            message.style.color = "lime";
            message.innerHTML = "✅ Login Successful";

            setTimeout(() => {

                window.location.href = "dashboard.html";

            }, 1000);

        }

        else {

            message.style.color = "red";
            message.innerHTML = "❌ " + result.detail;

        }

    }

    catch (error) {

        document.getElementById("message").style.color = "red";
        document.getElementById("message").innerHTML =
            "Unable to connect to the server.";

        console.error(error);

    }

});