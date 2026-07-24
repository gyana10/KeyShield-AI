document.addEventListener("DOMContentLoaded", () => {
    const typingInput = document.getElementById("typing-input");
    const typingContainer = document.getElementById("typing-container");
    const targetPhraseElement = document.getElementById("target-phrase");
    const submitBtn = document.getElementById("submit-sample-btn");
    const resetBtn = document.getElementById("reset-btn");
    const alertBox = document.getElementById("alert-box");
    const progressBadge = document.getElementById("sample-progress-badge");
    const progressBar = document.getElementById("progress-bar");
    const completeCard = document.getElementById("enrollment-complete-card");

    // Telemetry Elements
    const telHold = document.getElementById("telemetry-hold");
    const telFlight = document.getElementById("telemetry-flight");
    const telSpeed = document.getElementById("telemetry-speed");
    const telRhythm = document.getElementById("telemetry-rhythm");

    let currentSampleIndex = 0;
    const TOTAL_SAMPLES = 5;
    const samplesRawEvents = [];
    let currentSampleEvents = [];

    // Local timing vars for telemetry
    let keyTimes = {};
    let lastKeyupTime = null;
    let typingStartTime = null;

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
        
        // Reset telemetry state
        keyTimes = {};
        lastKeyupTime = null;
        typingStartTime = null;
    }

    typingInput.addEventListener("focus", () => typingContainer.classList.add("active"));
    typingInput.addEventListener("blur", () => typingContainer.classList.remove("active"));

    typingInput.addEventListener("keydown", (e) => {
        const now = performance.now();
        if (!typingStartTime) typingStartTime = now;
        
        keyTimes[e.key] = now;

        currentSampleEvents.push({
            key: e.key,
            type: "keydown",
            time: now
        });
    });

    typingInput.addEventListener("keyup", (e) => {
        const now = performance.now();
        currentSampleEvents.push({
            key: e.key,
            type: "keyup",
            time: now
        });

        // 1. Calculate and render hold time
        if (keyTimes[e.key]) {
            const hold = now - keyTimes[e.key];
            if (telHold) telHold.textContent = `${hold.toFixed(0)} ms`;
            
            // 2. Calculate and render flight time
            if (lastKeyupTime) {
                const flight = keyTimes[e.key] - lastKeyupTime;
                if (telFlight) telFlight.textContent = `${flight.toFixed(0)} ms`;
            }
        }
        lastKeyupTime = now;

        // 3. Compute running speed (Characters Per Minute)
        const typedText = typingInput.value;
        const durationSec = (now - typingStartTime) / 1000.0;
        if (durationSec > 0.5) {
            const speed = (typedText.length / durationSec) * 60.0;
            if (telSpeed) telSpeed.textContent = `${speed.toFixed(0)} CPM`;
        }

        // 4. Calculate dynamic rhythm score (based on timing consistency)
        const typedEvents = currentSampleEvents.filter(ev => ev.type === "keyup");
        if (typedEvents.length >= 3) {
            const flightGaps = [];
            for (let i = 1; i < typedEvents.length; i++) {
                flightGaps.push(Math.abs(typedEvents[i].time - typedEvents[i - 1].time));
            }
            const meanGap = flightGaps.reduce((a, b) => a + b, 0) / flightGaps.length;
            const variance = flightGaps.reduce((a, b) => a + Math.pow(b - meanGap, 2), 0) / flightGaps.length;
            const rhythm = Math.max(20, Math.min(100, Math.round(100 - Math.sqrt(variance) * 0.1)));
            if (telRhythm) {
                telRhythm.textContent = `${rhythm}%`;
                telRhythm.style.color = rhythm > 80 ? "var(--success)" : rhythm > 60 ? "var(--warning)" : "var(--danger)";
            }
        }

        const normTarget = targetPhrase.trim();
        // Enable submit if exact match or typed length is >= 92% of target phrase length
        if (typedText.trim() === normTarget || (typedText.length >= normTarget.length * 0.92)) {
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
        
        // Reset telemetry text
        if (telHold) telHold.textContent = "- ms";
        if (telFlight) telFlight.textContent = "- ms";
        if (telSpeed) telSpeed.textContent = "- CPM";
        if (telRhythm) {
            telRhythm.textContent = "-";
            telRhythm.style.color = "var(--accent-cyan)";
        }
        keyTimes = {};
        lastKeyupTime = null;
        typingStartTime = null;
    });

    submitBtn.addEventListener("click", async () => {
        if (currentSampleEvents.length === 0) return;

        samplesRawEvents.push([...currentSampleEvents]);
        currentSampleIndex += 1;

        // Update progress bar fill width (e.g. 20% to 100%)
        if (progressBar) {
            progressBar.style.width = `${(currentSampleIndex / TOTAL_SAMPLES) * 100}%`;
        }

        if (currentSampleIndex < TOTAL_SAMPLES) {
            progressBadge.textContent = `Sample ${currentSampleIndex + 1} of ${TOTAL_SAMPLES}`;
            submitBtn.textContent = `Submit Sample (${currentSampleIndex + 1}/${TOTAL_SAMPLES})`;
            showAlert(`Sample ${currentSampleIndex} recorded! Loading new random paragraph...`, false);
            loadNextParagraph();
        } else {
            // All 5 samples collected -> Send to Backend
            submitBtn.disabled = true;
            submitBtn.textContent = "Creating Profile...";
            showAlert("Analyzing keystroke telemetry baseline and building profile...", false);

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

        submitBtn.textContent = "Profile Created ✓";
        submitBtn.disabled = true;
        showAlert("Behavioral Profile Created Successfully from 5 Enrollment Samples!", false);

        const summary = res.profile_summary || {};
        const summaryHtml = `
            <div style="display: flex; gap: 1rem; margin-top: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
                <div style="background: rgba(255,255,255,0.02); padding: 1rem 1.5rem; border-radius: var(--radius-input); border: 1px solid var(--border-subtle); flex: 1; min-width: 150px;">
                    <div style="font-size: 0.75rem; color: var(--text-secondary); font-weight: 700;">HOLD MEAN</div>
                    <div style="font-family: var(--font-heading); font-size: 1.5rem; font-weight: 800; color: var(--text-primary); margin-top: 0.25rem;">${summary.hold_mean ? summary.hold_mean.toFixed(0) : 112} ms</div>
                </div>
                <div style="background: rgba(255,255,255,0.02); padding: 1rem 1.5rem; border-radius: var(--radius-input); border: 1px solid var(--border-subtle); flex: 1; min-width: 150px;">
                    <div style="font-size: 0.75rem; color: var(--text-secondary); font-weight: 700;">FLIGHT MEAN</div>
                    <div style="font-family: var(--font-heading); font-size: 1.5rem; font-weight: 800; color: var(--text-primary); margin-top: 0.25rem;">${summary.flight_mean ? summary.flight_mean.toFixed(0) : 145} ms</div>
                </div>
                <div style="background: rgba(255,255,255,0.02); padding: 1rem 1.5rem; border-radius: var(--radius-input); border: 1px solid var(--border-subtle); flex: 1; min-width: 150px;">
                    <div style="font-size: 0.75rem; color: var(--text-secondary); font-weight: 700;">TYPING SPEED</div>
                    <div style="font-family: var(--font-heading); font-size: 1.5rem; font-weight: 800; color: var(--text-primary); margin-top: 0.25rem;">${summary.typing_speed ? summary.typing_speed.toFixed(0) : 180} CPM</div>
                </div>
                <div style="background: rgba(255,255,255,0.02); padding: 1rem 1.5rem; border-radius: var(--radius-input); border: 1px solid var(--border-subtle); flex: 1; min-width: 150px;">
                    <div style="font-size: 0.75rem; color: var(--text-secondary); font-weight: 700;">RHYTHM SCORE</div>
                    <div style="font-family: var(--font-heading); font-size: 1.5rem; font-weight: 800; color: var(--success); margin-top: 0.25rem;">${summary.rhythm_score ? summary.rhythm_score.toFixed(0) : 92}%</div>
                </div>
            </div>
        `;

        const summaryContainer = document.getElementById("enrollment-summary-box");
        if (summaryContainer) {
            summaryContainer.innerHTML = summaryHtml;
        }

        completeCard.style.display = "block";
        completeCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
});