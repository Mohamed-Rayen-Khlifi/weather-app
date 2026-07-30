// ==========================
// Elements
// ==========================

const metricSelect =
    document.getElementById("metric-select");


const anomalyBtn =
    document.getElementById("anomaly-btn");


const summary =
    document.getElementById("anomalies-summary");


const container =
    document.getElementById("anomalies-data");




// ==========================
// Load Anomalies
// ==========================

async function loadAnomalies(){


    const metric =
        metricSelect.value;



    try {


        const response =
            await fetch(
                "/anomalies",
                {

                    method: "PUT",

                    headers: {

                        "Content-Type":
                        "application/json"

                    },


                    body: JSON.stringify({

                        metric: metric,

                        threshold: 2.0

                    })

                }
            );



        const data =
            await response.json();



        console.log(data);




        summary.innerHTML = `

            <h3>
                ${data.metric}
            </h3>


            <p>
                Mean:
                ${data.mean ?? "--"}
            </p>


            <p>
                Standard deviation:
                ${data.std ?? "--"}
            </p>


            <p>
                Threshold:
                ${data.threshold}
            </p>

        `;



        if(
            data.anomalies.length === 0
        ){


            container.innerHTML = `

                <div class="card">

                    <h3>
                        No anomalies detected
                    </h3>

                </div>

            `;


            return;

        }




        container.innerHTML =

            data.anomalies.map(a => `


                <div class="card">


                    <h3>
                        ⚠️ Anomaly detected
                    </h3>


                    <p>
                        Value:
                        ${a.value}
                    </p>


                    <p>
                        Z-score:
                        ${a.z_score}
                    </p>


                    <p>
                        Date:
                        ${a.recorded_at}
                    </p>


                </div>


            `).join("");



    }


    catch(error){


        console.error(
            "ERROR:",
            error
        );


        container.innerHTML = `

            <div class="card">

                Error loading anomalies

            </div>

        `;


    }


}




// ==========================
// Events
// ==========================

anomalyBtn.addEventListener(
    "click",
    loadAnomalies
);



// First load

loadAnomalies();