document
.getElementById("submitBtn")
.addEventListener("click", async function () {

    const features = extractFeatures(keyEvents);

    const response = await fetch(
        "http://127.0.0.1:8000/enroll",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(features)
        }
    );

    const result = await response.json();

    document
        .getElementById("status")
        .innerHTML = result.message;
});