async function loadHistory(){

    const container = document.getElementById("history-data");


    try{

        const response =
        await fetch("/measurements?metric=temperature&limit=20");


        const data = await response.json();


        container.innerHTML = data.map(item => `

            <div class="card">

                <p>
                Date: ${item.recorded_at}
                </p>

                <h3>
                ${item.value} °C
                </h3>

            </div>

        `).join("");

    }


    catch(error){

        console.error(error);

        container.innerHTML="Error loading history";

    }

}


loadHistory();