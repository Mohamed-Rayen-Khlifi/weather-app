// ==========================
// Elements
// ==========================

const metricSelect = document.getElementById("metric-select");
const forecastBtn = document.getElementById("forecast-btn");
const container = document.getElementById("forecast-data");

// ==========================
// Load Forecast
// ==========================

async function loadForecast() {

    const metric = metricSelect.value;

    try {

        const response = await fetch(
            "/forecast",
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

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const data = await response.json();

        console.log("Forecast data:", data);

        // ==========================
        // Not enough data
        // ==========================

        if (data.forecast === null) {

            container.innerHTML = `
                <div class="card">
                    <h3>${data.message}</h3>
                </div>
            `;

            return;
        }

        // ==========================
        // Forecast result
        // ==========================

        container.innerHTML = `

            <div class="card">

                <h2>
                    ${data.metric}
                </h2>

                <h1>
                    ${data.forecast} ${data.unit}
                </h1>

                <p>
                    Based on ${data.based_on} measurements
                </p>

                <p>
                    Last update:
                    ${data.last_update}
                </p>

            </div>

            <div class="card">

                <h3>
                    Previous values
                </h3>

                <ul>

                    ${
                        data.last_values.map(value => `
                            <li>
                                ${value} ${data.unit}
                            </li>
                        `).join("")
                    }

                </ul>

            </div>

        `;

    } catch (error) {

        console.error("Forecast error:", error);

        container.innerHTML = `
            <div class="card">
                <h3>Error loading forecast</h3>
            </div>
        `;
    }
}

// ==========================
// Button
// ==========================

if (forecastBtn) {

    forecastBtn.addEventListener(
        "click",
        loadForecast
    );

}

// ==========================
// First Load
// ==========================

loadForecast();