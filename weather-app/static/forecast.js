// ==========================
// Elements
// ==========================

const metricSelect =
    document.getElementById("metric-select");


const forecastBtn =
    document.getElementById("forecast-btn");


const container =
    document.getElementById("forecast-data");



// ==========================
// Load Forecast
// ==========================

async function loadForecast(){


    const metric =
        metricSelect.value;



    try {


        const response =
            await fetch(
                "/forecast",
                {

                    method: "PUT",

                    headers: {

                        "Content-Type":
                        "application/json"

                    },


                    body: JSON.stringify({

                        metric: metric

                    })

                }
            );



        const data =
            await response.json();




        if(data.forecast === null){


            container.innerHTML = `

                <div class="card">

                    <h3>
                        ${data.message}
                    </h3>

                </div>

            `;


            return;

        }




        container.innerHTML = `


            <div class="card">


                <h2>
                    ${data.metric}
                </h2>


                <h1>
                    ${data.forecast}
                    ${data.unit}
                </h1>



                <p>

                    Based on
                    ${data.based_on}
                    measurements

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
                                ${value}
                                ${data.unit}
                            </li>

                        `).join("")
                    }


                </ul>


            </div>


        `;



    }


    catch(error){


        console.error(error);


        container.innerHTML =

        "Error loading forecast";


    }


}




// ==========================
// Events
// ==========================


forecastBtn.addEventListener(
    "click",
    loadForecast
);



// First load

loadForecast();