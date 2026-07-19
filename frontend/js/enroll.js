document.addEventListener("DOMContentLoaded", async () => {
    if (!ApiClient.getToken()) {
        window.location.href = "login.html";
        return;
    }

    const typingInput = document.getElementById("typing-input");
    const typingContainer = document.getElementById("typing-container");
    const submitBtn = document.getElementById("submit-sample-btn");
    const resetBtn = document.getElementById("reset-btn");
    const sampleBadge = document.getElementById("sample-badge");
    const alertBox = document.getElementById("alert-box");

    const TARGET_PHRASE = "keyshield authentication dynamics";
    let events = [];

    function showAlert(msg, isError = true) {
        alertBox.style.display = "block";
        alertBox.textContent = msg;
        alertBox.className = isError ? "badge badge-high" : "badge badge-low";
        alertBox.style.width = "100%";
    }

    // Load initial enrollment state from profile API
    try {
        const profile = await ApiClient.getProfile();
        if (profile.sample_count >= 3) {
            sampleBadge.textContent = `Enrolled (${profile.sample_count} samples)`;
            sampleBadge.className = "badge badge-low";
        } else {
            sampleBadge.textContent = `Sample ${profile.sample_count + 1} of 3`;
        }
    } catch (e) {
        console.warn("Profile load error:", e);
    }

    typingInput.addEventListener("focus", () => {
        typingContainer.classList.add("active");
    });

    typingInput.addEventListener("blur", () => {
        typingContainer.classList.remove("active");
    });

    typingInput.addEventListener("keydown", (e) => {
        events.push({
            key: e.key,
            type: "keydown",
            time: performance.now()
        });
    });

    typingInput.addEventListener("keyup", (e) => {
        events.push({
            key: e.key,
            type: "keyup",
            time: performance.now()
        });

        if (typingInput.value.trim() === TARGET_PHRASE) {
            submitBtn.disabled = false;
            showAlert("Target phrase typed! Click 'Submit Sample' to save.", false);
        } else {
            submitBtn.disabled = true;
        }
    });

    resetBtn.addEventListener("click", () => {
        typingInput.value = "";
        events = [];
        submitBtn.disabled = true;
        alertBox.style.display = "none";
    });

    submitBtn.addEventListener("click", async () => {
        const keystrokeData = extractFeatures(events);
        try {
            submitBtn.disabled = true;
            submitBtn.textContent = "Submitting...";

            const res = await ApiClient.enroll(keystrokeData);

            if (res.enrollment_complete) {
                showAlert("🎉 Behavioral Profile Enrollment Complete! Redirecting...", false);
                sampleBadge.textContent = "Complete (3/3)";
                sampleBadge.className = "badge badge-low";
                setTimeout(() => {
                    window.location.href = "authenticate.html";
                }, 1500);
            } else {
                showAlert(`Sample ${res.sample_index}/3 saved! Please type the phrase again for sample ${res.sample_index + 1}.`, false);
                sampleBadge.textContent = `Sample ${res.sample_index + 1} of 3`;
                resetBtn.click();
            }
        } catch (err) {
            showAlert(err.message || "Failed to submit enrollment sample.");
            submitBtn.disabled = false;
        } finally {
            submitBtn.textContent = "Submit Sample";
        }
    });
});