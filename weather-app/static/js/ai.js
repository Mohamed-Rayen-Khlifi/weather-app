// ==========================
// Elements
// ==========================

const metricSelect =
    document.getElementById("ai-metric-select");


const aiBtn =
    document.getElementById("ai-btn");


const result =
    document.getElementById("ai-result");




// ==========================
// AI Prediction
// ==========================

async function predict(){


    const metric =
        metricSelect.value;



    try {


        const response =
            await fetch(
                "/ai/predict",
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



        if(data.prediction === null){


            result.innerHTML = `

                <h3>
                    ${data.message}
                </h3>

            `;


            return;

        }




        result.innerHTML = `


            <h2>
                ${data.metric}
            </h2>


            <h1>
                ${data.prediction}
            </h1>


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



    }


    catch(error){


        console.error(error);


        result.innerHTML =
        "Error loading AI prediction";


    }


}




// ==========================
// Event
// ==========================

aiBtn.addEventListener(
    "click",
    predict
);



// First load

predict();