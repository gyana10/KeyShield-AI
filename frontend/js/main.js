const API_BASE_URL = (window.location.origin.includes("localhost") || window.location.origin.includes("127.0.0.1"))
    ? "http://127.0.0.1:8000"
    : "https://keyshield-ai-backend.onrender.com";

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

class KeystrokeRecorder {
    constructor(inputElement, onCompleteCallback) {
        this.inputElement = inputElement;
        this.onCompleteCallback = onCompleteCallback;
        this.events = [];

        this.init();
    }

    init() {
        if (!this.inputElement) return;

        this.inputElement.addEventListener("keydown", (e) => {
            this.events.push({
                key: e.key,
                type: "keydown",
                time: performance.now()
            });
        });

        this.inputElement.addEventListener("keyup", (e) => {
            this.events.push({
                key: e.key,
                type: "keyup",
                time: performance.now()
            });

            if (this.onCompleteCallback) {
                this.onCompleteCallback(this.inputElement.value, this.events);
            }
        });
    }

    reset() {
        this.events = [];
        if (this.inputElement) {
            this.inputElement.value = "";
        }
    }

    getEvents() {
        return [...this.events];
    }
}
