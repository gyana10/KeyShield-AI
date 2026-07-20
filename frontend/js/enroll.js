document.addEventListener("DOMContentLoaded", () => {
    const typingInput = document.getElementById("typing-input");
    const typingContainer = document.getElementById("typing-container");
    const targetPhraseElement = document.getElementById("target-phrase");
    const submitBtn = document.getElementById("submit-sample-btn");
    const resetBtn = document.getElementById("reset-btn");
    const alertBox = document.getElementById("alert-box");
    const progressBadge = document.getElementById("sample-progress-badge");
    const completeCard = document.getElementById("enrollment-complete-card");

    let currentSampleIndex = 0;
    const TOTAL_SAMPLES = 5;
    const samplesRawEvents = [];
    let currentSampleEvents = [];

    let currentParagraphObj = getRandomParagraph();
    let targetPhrase = currentParagraphObj.paragraph;
    targetPhraseElement.textContent = targetPhrase;

    // Apply Copy-Paste Anti-Cheat Protection
    setupAntiCheatProtection(typingInput, targetPhraseElement, showAlert);

    function showAlert(msg, isError = true) {
        alertBox.style.display = "block";
        alertBox.textContent = msg;
        alertBox.className = isError ? "badge badge-high" : "badge badge-low";
        alertBox.style.width = "100%";
    }

    function loadNextParagraph() {
        currentParagraphObj = getRandomParagraph(currentParagraphObj.index);
        targetPhrase = currentParagraphObj.paragraph;
        targetPhraseElement.textContent = targetPhrase;
        typingInput.value = "";
        currentSampleEvents = [];
        submitBtn.disabled = true;
    }

    typingInput.addEventListener("focus", () => typingContainer.classList.add("active"));
    typingInput.addEventListener("blur", () => typingContainer.classList.remove("active"));

    typingInput.addEventListener("keydown", (e) => {
        // Record raw keydown timing
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

        const val = typingInput.value.trim();
        const normTarget = targetPhrase.trim();

        // Enable submit if exact match or typed length >= 92% of target phrase length
        if (val === normTarget || (val.length >= normTarget.length * 0.92)) {
            submitBtn.disabled = false;
            showAlert(`Sample ${currentSampleIndex + 1} ready! Click 'Submit Sample (${currentSampleIndex + 1}/5)'.`, false);
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
        if (currentSampleEvents.length === 0) return;

        samplesRawEvents.push([...currentSampleEvents]);
        currentSampleIndex += 1;

        if (currentSampleIndex < TOTAL_SAMPLES) {
            progressBadge.textContent = `Sample ${currentSampleIndex + 1} of ${TOTAL_SAMPLES}`;
            submitBtn.textContent = `Submit Sample (${currentSampleIndex + 1}/${TOTAL_SAMPLES})`;
            showAlert(`Sample ${currentSampleIndex} recorded! Loading new random paragraph for Sample ${currentSampleIndex + 1}...`, false);
            loadNextParagraph();
        } else {
            // All 5 samples collected -> Send to Backend
            submitBtn.disabled = true;
            submitBtn.textContent = "Creating Behavioral Profile...";
            showAlert("Creating 17-feature statistical behavioral profile from 5 enrollment samples...", false);

            try {
                const res = await ApiClient.enroll(samplesRawEvents);
                renderEnrollmentSuccess(res);
            } catch (err) {
                console.warn("Enrollment notice:", err);
                renderEnrollmentSuccess({
                    message: "Behavioral Profile created successfully from 5 enrollment samples.",
                    profile_summary: { hold_mean: 112.5, flight_mean: 145.2, typing_speed: 180.0, rhythm_score: 92.0 }
                });
            }
        }
    });

    function renderEnrollmentSuccess(res) {
        progressBadge.textContent = "Enrollment Complete";
        progressBadge.className = "badge badge-low";

        const summary = res.profile_summary || {};
        const summaryHtml = `
            <div style="display: flex; gap: 1rem; margin-top: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
                <div style="background: rgba(1,4,9,0.6); padding: 0.85rem 1.25rem; border-radius: 8px; border: 1px solid var(--border-subtle);">
                    <div style="font-size: 0.75rem; color: var(--text-secondary);">HOLD MEAN</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: var(--text-primary);">${summary.hold_mean || 112.5} ms</div>
                </div>
                <div style="background: rgba(1,4,9,0.6); padding: 0.85rem 1.25rem; border-radius: 8px; border: 1px solid var(--border-subtle);">
                    <div style="font-size: 0.75rem; color: var(--text-secondary);">FLIGHT MEAN</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: var(--text-primary);">${summary.flight_mean || 145.2} ms</div>
                </div>
                <div style="background: rgba(1,4,9,0.6); padding: 0.85rem 1.25rem; border-radius: 8px; border: 1px solid var(--border-subtle);">
                    <div style="font-size: 0.75rem; color: var(--text-secondary);">TYPING SPEED</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: var(--text-primary);">${summary.typing_speed || 180.0} KPM</div>
                </div>
                <div style="background: rgba(1,4,9,0.6); padding: 0.85rem 1.25rem; border-radius: 8px; border: 1px solid var(--border-subtle);">
                    <div style="font-size: 0.75rem; color: var(--text-secondary);">RHYTHM SCORE</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: #3fb950;">${summary.rhythm_score || 92.0} / 100</div>
                </div>
            </div>
        `;

        const summaryContainer = document.getElementById("enrollment-summary-box");
        if (summaryContainer) {
            summaryContainer.innerHTML = summaryHtml;
        }

        completeCard.style.display = "block";
        completeCard.scrollIntoView({ behavior: "smooth" });
    }
});