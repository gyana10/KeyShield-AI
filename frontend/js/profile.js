document.addEventListener("DOMContentLoaded", async () => {
    try {
        const profile = await ApiClient.getProfile();
        renderProfileData(profile);
    } catch (error) {
        console.warn("Using sample fallback profile data:", error);
        renderProfileData(getSampleProfile());
    }
});

function renderProfileData(data) {
    if (data.username) {
        document.getElementById("profile-username").textContent = `${data.username}'s Behavioral Profile`;
        document.getElementById("profile-avatar-letter").textContent = data.username.charAt(0).toUpperCase();
    }

    const meanHold = data.feature_means ? (data.feature_means.hold_mean || 112).toFixed(1) : "112.5";
    const meanFlight = data.feature_means ? (data.feature_means.flight_mean || 145).toFixed(1) : "145.2";
    const correction = data.feature_means ? ((data.feature_means.error_rate || 0.02) * 100).toFixed(1) : "2.1";
    const drift = ((data.drift_score || 0.012) * 100).toFixed(2);

    document.getElementById("stat-hold-mean").textContent = `${meanHold} ms`;
    document.getElementById("stat-flight-mean").textContent = `${meanFlight} ms`;
    document.getElementById("stat-correction").textContent = `${correction} %`;
    document.getElementById("stat-drift").textContent = `${drift} %`;

    if (data.created_at) {
        document.getElementById("profile-created").value = new Date(data.created_at).toLocaleString();
    } else {
        document.getElementById("profile-created").value = "Active Baseline";
    }

    if (data.updated_at) {
        document.getElementById("profile-updated").value = new Date(data.updated_at).toLocaleString();
    } else {
        document.getElementById("profile-updated").value = "Recently Updated";
    }

    renderProfileRadarChart(data.feature_means || {});
}

function renderProfileRadarChart(means) {
    const ctx = document.getElementById("profileRadarChart").getContext("2d");
    new Chart(ctx, {
        type: "radar",
        data: {
            labels: ["Hold Time", "Flight Time", "Press Duration", "Release Duration", "Correction Speed"],
            datasets: [{
                label: "Baseline Profile (ms)",
                data: [
                    means.hold_mean || 112,
                    means.flight_mean || 145,
                    means.press_duration || 120,
                    means.release_duration || 135,
                    (means.error_rate || 0.02) * 5000
                ],
                backgroundColor: "rgba(0, 113, 227, 0.25)",
                borderColor: "#0071e3",
                pointBackgroundColor: "#2997ff",
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: "rgba(255, 255, 255, 0.1)" },
                    grid: { color: "rgba(255, 255, 255, 0.1)" },
                    pointLabels: { color: "#86868b", font: { family: "-apple-system, BlinkMacSystemFont, sans-serif" } },
                    ticks: { display: false }
                }
            },
            plugins: {
                legend: { labels: { color: "#f5f5f7" } }
            }
        }
    });
}

function getSampleProfile() {
    return {
        username: "Demo User",
        drift_score: 0.014,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        feature_means: {
            hold_mean: 114.2,
            flight_mean: 148.5,
            error_rate: 0.018,
            press_duration: 122.0,
            release_duration: 138.4
        }
    };
}
