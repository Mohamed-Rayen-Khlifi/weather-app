// ==========================
// Elements
// ==========================

const metricSelect = document.getElementById("ai-metric-select");

const aiBtn = document.getElementById("ai-btn");

const result = document.getElementById("ai-result");

const anomalyResult = document.getElementById("anomaly-result");


// ==========================
// AI Prediction
// ==========================

async function predict() {

    const metric = metricSelect.value;

    result.innerHTML = "Loading prediction...";

    try {

        const response = await fetch(
            "/ai/predict",
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    metric: metric
                })
            }
        );

        const data = await response.json();

        if (data.prediction === null) {

            result.innerHTML = `
                <h3>${data.message}</h3>
            `;

            return;
        }

        result.innerHTML = `
            <h3>${data.metric}</h3>

            <h1>${data.prediction}</h1>

            <p>
                Model:
                ${data.model}
            </p>

            <p>
                Trained on:
                ${data.trained_on}
                measurements
            </p>
        `;

    } catch (error) {

        console.error(error);

        result.innerHTML =
            "Error loading AI prediction";
    }
}


// ==========================
// AI Anomaly Detection
// ==========================

async function detectAnomalies() {

    const metric = metricSelect.value;

    anomalyResult.innerHTML =
        "Detecting anomalies...";

    try {

        const response = await fetch(
            `/ai/anomalies/${metric}`
        );

        const data = await response.json();

        if (data.message) {

            anomalyResult.innerHTML = `
                <h3>${data.message}</h3>
            `;

            return;
        }

        if (data.anomalies_count === 0) {

            anomalyResult.innerHTML = `
                <h3>✅ No anomalies detected</h3>

                <p>
                    Analyzed:
                    ${data.total_records}
                    measurements
                </p>
            `;

            return;
        }

        let html = `
            <h3>
                ⚠️ ${data.anomalies_count}
                anomalies detected
            </h3>

            <p>
                Analyzed:
                ${data.total_records}
                measurements
            </p>

            <ul>
        `;

        data.anomalies.forEach(anomaly => {

            html += `
                <li>
                    <strong>
                        ${anomaly.value}
                    </strong>

                    <br>

                    Date:
                    ${anomaly.recorded_at}

                    <br>

                    Score:
                    ${anomaly.anomaly_score}
                </li>
            `;

        });

        html += `
            </ul>
        `;

        anomalyResult.innerHTML = html;

    } catch (error) {

        console.error(error);

        anomalyResult.innerHTML =
            "Error detecting anomalies";
    }
}


// ==========================
// Run AI
// ==========================

async function runAI() {

    await predict();

    await detectAnomalies();

}


// ==========================
// Event
// ==========================

aiBtn.addEventListener(
    "click",
    runAI
);


// ==========================
// First load
// ==========================

runAI();