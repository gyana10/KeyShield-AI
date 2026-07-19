const API_BASE_URL = window.location.origin.includes("localhost") || window.location.origin.includes("127.0.0.1")
    ? "http://127.0.0.1:8000"
    : window.location.origin;

class ApiClient {
    static getToken() {
        return localStorage.getItem("keyshield_token");
    }

    static setToken(token) {
        localStorage.setItem("keyshield_token", token);
    }

    static clearToken() {
        localStorage.removeItem("keyshield_token");
    }

    static getHeaders(auth = true) {
        const headers = {
            "Content-Type": "application/json"
        };
        if (auth) {
            const token = this.getToken();
            if (token) {
                headers["Authorization"] = `Bearer ${token}`;
            }
        }
        return headers;
    }

    static async request(endpoint, method = "GET", data = null, auth = true) {
        const options = {
            method,
            headers: this.getHeaders(auth)
        };
        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
            const resData = await response.json();

            if (!response.ok) {
                if (response.status === 401 && auth) {
                    this.clearToken();
                    window.location.href = "login.html";
                }
                throw new Error(resData.detail || "API Request Failed");
            }
            return resData;
        } catch (error) {
            console.error(`API Error [${endpoint}]:`, error);
            throw error;
        }
    }

    static async register(username, email, password) {
        return this.request("/register", "POST", { username, email, password }, false);
    }

    static async login(email, password) {
        const res = await this.request("/login", "POST", { email, password }, false);
        if (res.access_token) {
            this.setToken(res.access_token);
        }
        return res;
    }

    static async enroll(keystrokeData) {
        return this.request("/enroll", "POST", keystrokeData, true);
    }

    static async authenticate(keystrokeData) {
        return this.request("/authenticate", "POST", keystrokeData, true);
    }

    static async getHistory(limit = 20, offset = 0) {
        return this.request(`/history?limit=${limit}&offset=${offset}`, "GET", null, true);
    }

    static async getProfile() {
        return this.request("/profile", "GET", null, true);
    }

    static async getModelInfo() {
        return this.request("/model-info", "GET", null, true);
    }

    static async getStatistics() {
        return this.request("/statistics", "GET", null, true);
    }
}
