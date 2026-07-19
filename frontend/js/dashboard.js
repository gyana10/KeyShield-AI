document.addEventListener("DOMContentLoaded", async () => {
    if (!ApiClient.getToken()) {
        window.location.href = "login.html";
        return;
    }

    const logoutBtn = document.getElementById("logout-btn");
    logoutBtn.addEventListener("click", () => {
        ApiClient.clearToken();
        window.location.href = "login.html";
    });

    const statTotal = document.getElementById("stat-total");
    const statPassRate = document.getElementById("stat-pass-rate");
    const statAvgSim = document.getElementById("stat-avg-sim");
    const statDrift = document.getElementById("stat-drift");
    const historyTableBody = document.getElementById("history-table-body");

    // Configure Chart.js default fonts and colors for Glassmorphic dark mode
    Chart.defaults.color = "#94a3b8";
    Chart.defaults.font.family = "'Inter', sans-serif";

    try {
        // Fetch all dashboard data concurrently
        const [stats, profile, history, modelInfo] = await Promise.all([
            ApiClient.getStatistics(),
            ApiClient.getProfile(),
            ApiClient.getHistory(20, 0),
            ApiClient.getModelInfo()
        ]);

        // Populate Summary Stats
        statTotal.textContent = stats.total_authentications;
        statPassRate.textContent = `${stats.pass_rate}%`;
        statAvgSim.textContent = `${stats.average_similarity}%`;
        statDrift.textContent = stats.drift_status.replace(/_/g, " ");

        // 1. Render Radar Chart (Profile vs Recent Attempt)
        renderRadarChart(profile, history.logs[0]);

        // 2. Render Donut Chart (Risk Distribution)
        renderDonutChart(stats.risk_breakdown);

        // 3. Render Authentication Timeline
        renderTimelineChart(history.logs);

        // 4. Render Global Tree SHAP Feature Importance
        renderShapChart(modelInfo.global_feature_importance);

        // 5. Render Model Performance Comparison
        renderModelCompChart(modelInfo.model_comparison);

        // Populate History Table
        renderHistoryTable(history.logs);

    } catch (err) {
        console.error("Dashboard Loading Error:", err);
    }
});

function renderRadarChart(profile, latestLog) {
    const ctx = document.getElementById("radarChart").getContext("2d");
    
    const labels = ["Hold Mean", "Hold Std", "Flight Mean", "Flight Std", "Total Duration"];
    const profileData = [
        profile.hold_mean || 0.1,
        profile.hold_std || 0.02,
        profile.flight_mean || 0.2,
        profile.flight_std || 0.05,
        profile.total_duration || 3.0
    ];

    let attemptData = [...profileData];
    if (latestLog && latestLog.shap_explanation && latestLog.shap_explanation.local_contributions) {
        const local = latestLog.shap_explanation.local_contributions;
        attemptData = [
            profileData[0] + (local["hold_mean"] || 0.0),
            profileData[1] + (local["hold_std"] || 0.0),
            profileData[2] + (local["flight_mean"] || 0.0),
            profileData[3] + (local["flight_std"] || 0.0),
            profileData[4] + (local["total_duration"] || 0.0)
        ];
    }

    new Chart(ctx, {
        type: "radar",
        data: {
            labels,
            datasets: [
                {
                    label: "User Profile Baseline",
                    data: profileData,
                    borderColor: "#06b6d4",
                    backgroundColor: "rgba(6, 182, 212, 0.2)",
                    borderWidth: 2
                },
                {
                    label: "Latest Authentication Attempt",
                    data: attemptData,
                    borderColor: "#8b5cf6",
                    backgroundColor: "rgba(139, 92, 246, 0.2)",
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    grid: { color: "rgba(255, 255, 255, 0.08)" },
                    angleLines: { color: "rgba(255, 255, 255, 0.08)" },
                    pointLabels: { color: "#94a3b8" }
                }
            }
        }
    });
}

function renderDonutChart(riskBreakdown) {
    const ctx = document.getElementById("donutChart").getContext("2d");
    
    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Low Risk", "Medium Risk", "High Risk"],
            datasets: [{
                data: [riskBreakdown.LOW || 0, riskBreakdown.MEDIUM || 0, riskBreakdown.HIGH || 0],
                backgroundColor: ["#10b981", "#f59e0b", "#f43f5e"],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom" }
            }
        }
    });
}

function renderTimelineChart(logs) {
    const ctx = document.getElementById("timelineChart").getContext("2d");
    const reversedLogs = [...logs].reverse();

    const labels = reversedLogs.map(l => new Date(l.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
    const simData = reversedLogs.map(l => l.profile_similarity);
    const confData = reversedLogs.map(l => l.confidence_score);

    new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [
                {
                    label: "Profile Similarity (%)",
                    data: simData,
                    borderColor: "#06b6d4",
                    backgroundColor: "rgba(6, 182, 212, 0.1)",
                    fill: true,
                    tension: 0.3
                },
                {
                    label: "Confidence Score (%)",
                    data: confData,
                    borderColor: "#10b981",
                    backgroundColor: "transparent",
                    borderDash: [5, 5],
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false } },
                y: { min: 0, max: 100, grid: { color: "rgba(255, 255, 255, 0.05)" } }
            }
        }
    });
}

function renderShapChart(globalImportance) {
    const ctx = document.getElementById("shapChart").getContext("2d");
    const sorted = Object.entries(globalImportance || {}).sort((a, b) => b[1] - a[1]);

    const labels = sorted.map(item => item[0]);
    const data = sorted.map(item => item[1]);

    new Chart(ctx, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Tree SHAP Importance",
                data,
                backgroundColor: "rgba(139, 92, 246, 0.7)",
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            scales: {
                x: { grid: { color: "rgba(255, 255, 255, 0.05)" } },
                y: { grid: { display: false } }
            }
        }
    });
}

function renderModelCompChart(modelComp) {
    const ctx = document.getElementById("modelCompChart").getContext("2d");

    const labels = modelComp.map(m => m.model_name);
    const accData = modelComp.map(m => (m.accuracy * 100).toFixed(1));
    const aucData = modelComp.map(m => (m.roc_auc * 100).toFixed(1));

    new Chart(ctx, {
        type: "bar",
        data: {
            labels,
            datasets: [
                {
                    label: "Accuracy (%)",
                    data: accData,
                    backgroundColor: "rgba(6, 182, 212, 0.8)",
                    borderRadius: 6
                },
                {
                    label: "ROC-AUC (%)",
                    data: aucData,
                    backgroundColor: "rgba(16, 185, 129, 0.8)",
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false } },
                y: { min: 70, max: 100, grid: { color: "rgba(255, 255, 255, 0.05)" } }
            }
        }
    });
}

function renderHistoryTable(logs) {
    if (!logs || logs.length === 0) {
        historyTableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-dim);">No authentication records found.</td></tr>`;
        return;
    }

    historyTableBody.innerHTML = logs.map(l => {
        const dateStr = new Date(l.created_at).toLocaleString();
        const decisionBadge = l.decision === "GENUINE"
            ? `<span class="badge badge-low">GENUINE</span>`
            : `<span class="badge badge-high">SUSPICIOUS</span>`;

        let riskBadge = `<span class="badge badge-low">LOW</span>`;
        if (l.risk === "MEDIUM") riskBadge = `<span class="badge badge-medium">MEDIUM</span>`;
        else if (l.risk === "HIGH") riskBadge = `<span class="badge badge-high">HIGH</span>`;

        const shapText = l.shap_explanation ? (l.shap_explanation.text_explanation || "Keystroke evaluated") : "-";

        return `
            <tr>
                <td>#${l.id}</td>
                <td>${dateStr}</td>
                <td>${decisionBadge}</td>
                <td>${riskBadge}</td>
                <td>${l.confidence_score}%</td>
                <td>${l.profile_similarity}%</td>
                <td>${(l.probability * 100).toFixed(1)}%</td>
                <td style="font-size: 0.8rem; color: var(--text-muted); max-width: 250px;">${shapText}</td>
            </tr>
        `;
    }).join("");
}
