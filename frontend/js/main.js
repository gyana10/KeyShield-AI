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

// -------------------------------------------------------------
// Interactive Three.js Background wave/particle simulator
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("threejs-bg");
    if (!canvas) return;

    if (typeof THREE === "undefined") {
        console.warn("Three.js library not loaded.");
        return;
    }

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.z = 220;

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Particle network
    const particleCount = 650;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const colorBlue = new THREE.Color("#3B82F6");
    const colorCyan = new THREE.Color("#22D3EE");

    for (let i = 0; i < particleCount; i++) {
        positions[i * 3] = (Math.random() - 0.5) * 600;
        positions[i * 3 + 1] = (Math.random() - 0.5) * 600;
        positions[i * 3 + 2] = (Math.random() - 0.5) * 300;

        const mixedColor = colorBlue.clone().lerp(colorCyan, Math.random());
        colors[i * 3] = mixedColor.r;
        colors[i * 3 + 1] = mixedColor.g;
        colors[i * 3 + 2] = mixedColor.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    // Circular particle texture generator
    const pCanvas = document.createElement('canvas');
    pCanvas.width = 16;
    pCanvas.height = 16;
    const ctx = pCanvas.getContext('2d');
    const grad = ctx.createRadialGradient(8, 8, 0, 8, 8, 8);
    grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
    grad.addColorStop(1, 'rgba(255, 255, 255, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 16, 16);
    const texture = new THREE.CanvasTexture(pCanvas);

    const material = new THREE.PointsMaterial({
        size: 4,
        vertexColors: true,
        transparent: true,
        opacity: 0.5,
        map: texture,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // Wave grid lines
    const lineCount = 24;
    const lineGeometry = new THREE.BufferGeometry();
    const linePositions = [];
    const lineColors = [];

    for (let j = 0; j < lineCount; j++) {
        const xOffset = (j - lineCount/2) * 25;
        for (let k = 0; k < 35; k++) {
            const zVal = (k - 17) * 18;
            linePositions.push(xOffset, 0, zVal);
            lineColors.push(colorBlue.r, colorBlue.g, colorBlue.b);
        }
    }

    lineGeometry.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
    lineGeometry.setAttribute('color', new THREE.Float32BufferAttribute(lineColors, 3));

    const lineMat = new THREE.LineBasicMaterial({
        vertexColors: true,
        transparent: true,
        opacity: 0.12,
        blending: THREE.AdditiveBlending
    });

    const gridLines = new THREE.Line(lineGeometry, lineMat);
    scene.add(gridLines);

    const clock = new THREE.Clock();

    const animate = () => {
        requestAnimationFrame(animate);

        const elapsed = clock.getElapsedTime();

        // Wave vertex computation
        const posAttr = gridLines.geometry.attributes.position;
        const count = posAttr.count;
        for (let i = 0; i < count; i++) {
            const x = posAttr.getX(i);
            const z = posAttr.getZ(i);
            const y = Math.sin(x * 0.015 + elapsed * 1.3) * 12 + Math.cos(z * 0.01 + elapsed * 1.1) * 8;
            posAttr.setY(i, y);
        }
        gridLines.geometry.attributes.position.needsUpdate = true;

        particles.rotation.y = elapsed * 0.02;
        particles.rotation.x = elapsed * 0.01;

        camera.position.x = Math.sin(elapsed * 0.15) * 20;
        camera.position.y = Math.cos(elapsed * 0.08) * 12;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
    };

    animate();

    window.addEventListener("resize", () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
});
