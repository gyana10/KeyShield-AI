document.addEventListener("DOMContentLoaded", () => {
    if (!ApiClient.getToken()) {
        window.location.href = "login.html";
        return;
    }

    const typingInput = document.getElementById("typing-input");
    const typingContainer = document.getElementById("typing-container");
    const authBtn = document.getElementById("auth-btn");
    const resetBtn = document.getElementById("reset-btn");
    const alertBox = document.getElementById("alert-box");

    const resultCard = document.getElementById("result-card");
    const riskBadge = document.getElementById("risk-badge");
    const resDecision = document.getElementById("res-decision");
    const resConfidence = document.getElementById("res-confidence");
    const resSimilarity = document.getElementById("res-similarity");
    const resProb = document.getElementById("res-prob");
    const resShapText = document.getElementById("res-shap-text");

    const TARGET_PHRASE = "keyshield authentication dynamics";
    let events = [];

    function showAlert(msg, isError = true) {
        alertBox.style.display = "block";
        alertBox.textContent = msg;
        alertBox.className = isError ? "badge badge-high" : "badge badge-low";
        alertBox.style.width = "100%";
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
            authBtn.disabled = false;
            showAlert("Target phrase complete. Click 'Authenticate' to classify biometrics.", false);
        } else {
            authBtn.disabled = true;
        }
    });

    resetBtn.addEventListener("click", () => {
        typingInput.value = "";
        events = [];
        authBtn.disabled = true;
        alertBox.style.display = "none";
        resultCard.style.display = "none";
    });

    authBtn.addEventListener("click", async () => {
        const keystrokeData = extractFeatures(events);

        try {
            authBtn.disabled = true;
            authBtn.textContent = "Analyzing...";

            const res = await ApiClient.authenticate(keystrokeData);

            // Populate Result Card
            resDecision.textContent = res.decision;
            resDecision.style.color = res.decision === "GENUINE" ? "var(--success)" : "var(--danger)";

            riskBadge.textContent = `${res.risk} RISK`;
            if (res.risk === "LOW") riskBadge.className = "badge badge-low";
            else if (res.risk === "MEDIUM") riskBadge.className = "badge badge-medium";
            else riskBadge.className = "badge badge-high";

            resConfidence.textContent = `${res.confidence_score}%`;
            resSimilarity.textContent = `${res.profile_similarity}%`;
            resProb.textContent = `${(res.probability * 100).toFixed(1)}%`;

            resShapText.textContent = res.shap_explanation ? res.shap_explanation.text_explanation : "Feature values evaluated.";

            resultCard.style.display = "block";
            resultCard.scrollIntoView({ behavior: "smooth" });
        } catch (err) {
            showAlert(err.message || "Authentication evaluation failed.");
        } finally {
            authBtn.disabled = false;
            authBtn.textContent = "Authenticate";
        }
    });
});