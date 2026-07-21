async function loadAnomalies(){

    const container =
    document.getElementById("anomalies-data");


    try{

        const response =
        await fetch("/anomalies");


        const data =
        await response.json();


        if(data.anomalies.length === 0){

            container.innerHTML =
            "<h3>No anomalies detected</h3>";

            return;

        }


        container.innerHTML =
        data.anomalies.map(a => `

            <div class="card">

                <p>
                Value: ${a.value}
                </p>

                <p>
                Z-score: ${a.z_score}
                </p>

            </div>

        `).join("");

    }


    catch(error){

        console.error(error);

        container.innerHTML =
        "Error loading anomalies";

    }

}


loadAnomalies();