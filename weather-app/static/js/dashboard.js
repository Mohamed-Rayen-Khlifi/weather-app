// ==========================
// Elements
// ==========================

const tempValue = document.getElementById("temp-value");
const tempTime = document.getElementById("temp-time");

const humidityValue = document.getElementById("humidity-value");
const humidityTime = document.getElementById("humidity-time");

const windValue = document.getElementById("wind-value");
const windTime = document.getElementById("wind-time");

const pressureValue = document.getElementById("pressure-value");
const pressureTime = document.getElementById("pressure-time");

const refreshBtn = document.getElementById("refreshBtn");

const chartCanvas = document.getElementById("tempChart");

let chart = null;


// ==========================
// Get latest measurement
// ==========================

async function getLatest(metric) {

    try {

        const response = await fetch(
            `/measurements/latest?metric=${metric}`
        );


        if (!response.ok) {

            console.error(
                "Error getting",
                metric
            );

            return null;
        }


        return await response.json();


    } catch(error) {

        console.error(error);

        return null;

    }

}



// ==========================
// Get history
// ==========================

async function getHistory(
    metric = "temperature",
    limit = 20
) {

    try {

        const response = await fetch(
            `/measurements?metric=${metric}&limit=${limit}`
        );


        if (!response.ok) {

            return [];

        }


        return await response.json();


    } catch(error) {

        console.error(error);

        return [];

    }

}



// ==========================
// Update dashboard
// ==========================

async function updateDashboard(){


    const temperature =
        await getLatest("temperature");


    const humidity =
        await getLatest("humidity");


    const wind =
        await getLatest("windspeed");


    const pressure =
        await getLatest("pressure");



    if(temperature){

        tempValue.textContent =
            `${temperature.value} °C`;

        tempTime.textContent =
            new Date(
                temperature.recorded_at
            ).toLocaleString();

    }



    if(humidity){

        humidityValue.textContent =
            `${humidity.value} %`;

        humidityTime.textContent =
            new Date(
                humidity.recorded_at
            ).toLocaleString();

    }



    if(wind){

        windValue.textContent =
            `${wind.value} km/h`;

        windTime.textContent =
            new Date(
                wind.recorded_at
            ).toLocaleString();

    }



    if(pressure){

        pressureValue.textContent =
            `${pressure.value} hPa`;

        pressureTime.textContent =
            new Date(
                pressure.recorded_at
            ).toLocaleString();

    }



    const history =
        await getHistory(
            "temperature",
            20
        );


    drawChart(history);

}



// ==========================
// Draw chart
// ==========================

function drawChart(history){


    if(!chartCanvas){

        return;

    }


    const labels =
        history.map(item =>
            new Date(
                item.recorded_at
            ).toLocaleTimeString()
        );


    const values =
        history.map(
            item => item.value
        );



    if(chart){

        chart.destroy();

    }



    chart = new Chart(
        chartCanvas,
        {

            type:"line",

            data:{

                labels:labels,

                datasets:[

                    {

                        label:
                        "Temperature °C",

                        data:values,

                        fill:false,

                        tension:0.3,

                        borderWidth:2

                    }

                ]

            },


            options:{

                responsive:true,

                maintainAspectRatio:false

            }

        }

    );

}



// ==========================
// Events
// ==========================

if(refreshBtn){

    refreshBtn.addEventListener(
        "click",
        updateDashboard
    );

}


// First load

updateDashboard();


// Auto refresh every minute

setInterval(
    updateDashboard,
    60000
);