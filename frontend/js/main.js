const API_BASE_URL = (window.location.origin.includes("localhost") || window.location.origin.includes("127.0.0.1"))
    ? "http://127.0.0.1:8000"
    : "https://keyshield-ai-backend.onrender.com";

const PARAGRAPH_BANK = [
    "Artificial intelligence and continuous biometrics protect modern enterprise software systems from credential abuse.",
    "Keystroke dynamics measure unique timing patterns in hold times and flight transitions while typing.",
    "Commercial authentication platforms analyze behavioral features to verify identity without intrusive passwords.",
    "Machine learning models evaluate keystroke variance to distinguish legitimate users from malicious automated bots.",
    "Isolation forest anomaly detection identifies out of distribution timing samples during live verification attempts.",
    "Stacking ensemble architecture combines random forest xgboost and lightgbm models for high classification accuracy.",
    "Tree SHAP explainability provides clear natural language justifications for every automated authentication decision.",
    "Adaptive behavioral profiles update continuously using exponential moving average logic for genuine sessions.",
    "Zero trust security frameworks enforce multi factor behavioral verification across distributed cloud applications.",
    "Keystroke hold duration represents the precise millisecond time interval a physical key remains depressed.",
    "Flight time measures the latency interval between releasing one key and pressing the subsequent character.",
    "Behavioral biometrics offers frictionless security by monitoring user interaction patterns silently in the background.",
    "Cybersecurity teams deploy machine learning models to detect credential theft and session hijacking attempts.",
    "Feature engineering converts raw keydown and keyup timing events into high dimensional statistical vectors.",
    "Random forest models aggregate decision trees to classify complex behavioral typing patterns reliably.",
    "XGBoost gradient boosting optimizes loss functions to capture subtle non linear keystroke timing variations.",
    "LightGBM offers fast tree based feature partitioning for large scale behavioral telemetry streams.",
    "Logistic regression meta learners aggregate base model probability vectors into a unified decision score.",
    "Out of fold predictions prevent data leakage during multi model stacking ensemble training procedures.",
    "Statistical baseline tolerances establish expected minimum maximum and standard deviation ranges for users.",
    "Keystroke rhythm stability measures timing consistency across successive character transitions during typing.",
    "Multi layer verification engines combine profile similarity isolation forest and ensemble probability scores.",
    "Behavioral biometrics eliminates reliance on static credentials that can be leaked or stolen by hackers.",
    "Continuous session monitoring ensures identity confidence remains high throughout the entire user application session.",
    "KeyShield AI delivers recruiter grade behavioral biometric security with explainable artificial intelligence."
];

function getRandomParagraph(excludeIndex = -1) {
    let index;
    do {
        index = Math.floor(Math.random() * PARAGRAPH_BANK.length);
    } while (index === excludeIndex && PARAGRAPH_BANK.length > 1);
    return { paragraph: PARAGRAPH_BANK[index], index };
}

function setupAntiCheatProtection(inputElement, paragraphElement, alertCallback) {
    if (paragraphElement) {
        paragraphElement.style.userSelect = "none";
        paragraphElement.style.webkitUserSelect = "none";
        paragraphElement.style.mozUserSelect = "none";
        paragraphElement.style.msUserSelect = "none";
        paragraphElement.addEventListener("copy", (e) => {
            e.preventDefault();
            if (alertCallback) alertCallback("Copying paragraph text is prohibited.", true);
        });
    }

    if (inputElement) {
        const preventPaste = (e) => {
            e.preventDefault();
            inputElement.value = "";
            if (alertCallback) {
                alertCallback("Copy-pasting is strictly prohibited! Please type the paragraph manually.", true);
            }
        };

        inputElement.addEventListener("paste", preventPaste);
        inputElement.addEventListener("copy", (e) => e.preventDefault());
        inputElement.addEventListener("cut", (e) => e.preventDefault());
        inputElement.addEventListener("drop", preventPaste);
        inputElement.addEventListener("contextmenu", (e) => e.preventDefault());
    }
}

class ApiClient {
    static async request(endpoint, method = "GET", data = null) {
        const options = {
            method,
            headers: {
                "Content-Type": "application/json"
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
            const resData = await response.json();

            if (!response.ok) {
                throw new Error(resData.detail || "API Request Failed");
            }
            return resData;
        } catch (error) {
            console.error(`API Error [${endpoint}]:`, error);
            throw error;
        }
    }

    static async enroll(samples) {
        return this.request("/enroll", "POST", { samples });
    }

    static async authenticate(events) {
        return this.request("/authenticate", "POST", { events });
    }

    static async getProfile() {
        return this.request("/profile", "GET");
    }

    static async getHistory(limit = 20, offset = 0) {
        return this.request(`/history?limit=${limit}&offset=${offset}`, "GET");
    }

    static async getModelInfo() {
        return this.request("/model-info", "GET");
    }

    static async getStatistics() {
        return this.request("/statistics", "GET");
    }
}
