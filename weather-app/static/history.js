async function loadHistory(){

    const container =
    document.getElementById("history-data");


    try {


        const response =
        await fetch(
            "/measurements?metric=temperature&limit=20"
        );


        const data =
        await response.json();



        // Cards

        container.innerHTML = data.map(item => `

            <div class="card">

                <p>
                    ${item.recorded_at}
                </p>

                <h2>
                    ${item.value} °C
                </h2>

            </div>


        `).join("");



        // Chart

        const labels =
        data.map(
            item =>
            new Date(item.recorded_at)
            .toLocaleTimeString()
        );



        const values =
        data.map(
            item =>
            item.value
        );



        const ctx =
        document.getElementById(
            "historyChart"
        );


        new Chart(ctx, {

            type: "line",


            data: {

                labels: labels,


                datasets: [{

                    label:
                    "Temperature °C",


                    data: values,


                    tension: 0.3

                }]

            },


            options: {

                responsive: true

            }

        });



    }


    catch(error){

        console.error(error);

        container.innerHTML =
        "Error loading history";

    }


}



loadHistory();