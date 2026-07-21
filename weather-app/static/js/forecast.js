async function loadForecast(){

    const container = document.getElementById("forecast-data");

    try {

        const response = await fetch("/forecast");

        const data = await response.json();

        container.innerHTML = `

            <div class="card">

                <h2>${data.metric}</h2>

                <h3>${data.forecast} °C</h3>

                <p>
                    Based on ${data.based_on} measurements
                </p>

            </div>

        `;

    } catch(error) {

        console.error(error);

        container.innerHTML = "Error loading forecast";

    }

}


loadForecast();