 console.log("ANOMALIES JS LOADED");
 async function loadAnomalies(){

    const container = document.getElementById("anomalies-data");

    try {

        const response = await fetch("/anomalies");

        const data = await response.json();

        console.log(data);


        if(data.anomalies.length === 0){

            container.innerHTML = `
                <div class="card">
                    <h3>No anomalies detected</h3>
                </div>
            `;

            return;
        }


        container.innerHTML = data.anomalies.map(a => `

            <div class="card">

                <h3>⚠️ Anomaly detected</h3>

                <p>
                    Value: ${a.value}
                </p>

                <p>
                    Z-score: ${a.z_score}
                </p>

            </div>

        `).join("");


    } catch(error){

        console.error("ERROR:", error);

        container.innerHTML = `
            <h3>Error loading anomalies</h3>
        `;
    }

}


loadAnomalies();