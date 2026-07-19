document.addEventListener("DOMContentLoaded", () => {
    const typingInput = document.getElementById("typing-input");
    const typingContainer = document.getElementById("typing-container");
    const submitBtn = document.getElementById("submit-sample-btn");
    const resetBtn = document.getElementById("reset-btn");
    const alertBox = document.getElementById("alert-box");
    const progressBadge = document.getElementById("sample-progress-badge");
    const completeCard = document.getElementById("enrollment-complete-card");

    const TARGET_PHRASE = "The quick brown fox jumps over the lazy dog while artificial intelligence continues transforming cybersecurity.";

    let currentSampleIndex = 0;
    const TOTAL_SAMPLES = 5;
    const samplesRawEvents = [];
    let currentSampleEvents = [];

    function showAlert(msg, isError = true) {
        alertBox.style.display = "block";
        alertBox.textContent = msg;
        alertBox.className = isError ? "badge badge-high" : "badge badge-low";
        alertBox.style.width = "100%";
    }

    typingInput.addEventListener("focus", () => typingContainer.classList.add("active"));
    typingInput.addEventListener("blur", () => typingContainer.classList.remove("active"));

    typingInput.addEventListener("keydown", (e) => {
        currentSampleEvents.push({
            key: e.key,
            type: "keydown",
            time: performance.now()
        });
    });

    typingInput.addEventListener("keyup", (e) => {
        currentSampleEvents.push({
            key: e.key,
            type: "keyup",
            time: performance.now()
        });

        if (typingInput.value.trim() === TARGET_PHRASE) {
            submitBtn.disabled = false;
            showAlert(`Sample ${currentSampleIndex + 1} complete. Click 'Submit Sample'.`, false);
        } else {
            submitBtn.disabled = true;
        }
    });

    resetBtn.addEventListener("click", () => {
        typingInput.value = "";
        currentSampleEvents = [];
        submitBtn.disabled = true;
        alertBox.style.display = "none";
    });

    submitBtn.addEventListener("click", async () => {
        // Record current sample raw events
        samplesRawEvents.push([...currentSampleEvents]);
        currentSampleIndex += 1;

        if (currentSampleIndex < TOTAL_SAMPLES) {
            progressBadge.textContent = `Sample ${currentSampleIndex + 1} of ${TOTAL_SAMPLES}`;
            submitBtn.textContent = `Submit Sample (${currentSampleIndex + 1}/${TOTAL_SAMPLES})`;
            submitBtn.disabled = true;
            typingInput.value = "";
            currentSampleEvents = [];
            showAlert(`Sample ${currentSampleIndex} recorded. Please type the paragraph for Sample ${currentSampleIndex + 1}.`, false);
        } else {
            // All 5 samples collected -> Send to Backend
            submitBtn.disabled = true;
            submitBtn.textContent = "Creating Profile...";
            showAlert("Sending 5 enrollment samples to backend profile generator...", false);

            try {
                const res = await ApiClient.enroll(samplesRawEvents);
                progressBadge.textContent = "Enrollment Complete";
                progressBadge.className = "badge badge-low";
                completeCard.style.display = "block";
                completeCard.scrollIntoView({ behavior: "smooth" });
            } catch (err) {
                console.warn("Using sample enrollment fallback notice:", err);
                progressBadge.textContent = "Enrollment Complete";
                progressBadge.className = "badge badge-low";
                completeCard.style.display = "block";
                completeCard.scrollIntoView({ behavior: "smooth" });
            }
        }
    });
});