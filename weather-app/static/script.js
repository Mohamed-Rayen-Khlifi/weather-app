const tempValue = document.getElementById('temp-value');
const tempTime = document.getElementById('temp-time');
const humidityValue = document.getElementById('humidity-value');
const humidityTime = document.getElementById('humidity-time');
const windValue = document.getElementById('wind-value');
const windTime = document.getElementById('wind-time');
const pressureValue = document.getElementById('pressure-value');
const pressureTime = document.getElementById('pressure-time');
const refreshBtn = document.getElementById('refreshBtn');

let chart = null;
async function fetchLatestMetric(metric) {
    try {
        const res = await fetch(/measurements/latest?metric=${metric});
        if (!res.ok) return null;
        return await res.json();
    } catch (e) {
        console.warn(Pas de données pour ${metric});
        return null;
    }
}

async function fetchHistory(metric = 'temperature', limit = 20) {
    try {
        const res = await fetch(/measurements?metric=${metric}&limit=${limit});
        if (!res.ok) return [];
        return await res.json();
    } catch (e) {
        console.error(' Erreur historique:', e);
        return [];
    }
}

async function updateDashboard(){ 

   const temp = await fetchLatestMetric('temperature');
    const humidity = await fetchLatestMetric('humidity');
    const wind = await fetchLatestMetric('windspeed');
    const pressure = await fetchLatestMetric('pressure');
    if (temp) {
        tempValue.textContent = temp.value + ' °C';
        tempTime.textContent = new Date(temp.recorded_at).toLocaleString('fr-FR');
    }
    if (humidity) {
        humidityValue.textContent = humidity.value + ' %';
        humidityTime.textContent = new Date(humidity.recorded_at).toLocaleString('fr-FR');
    }
    if (wind) {
        windValue.textContent = wind.value + ' km/h';
        windTime.textContent = new Date(wind.recorded_at).toLocaleString('fr-FR');
    }
    if (pressure) {
        pressureValue.textContent = pressure.value + ' hPa';
        pressureTime.textContent = new Date(pressure.recorded_at).toLocaleString('fr-FR');
    }
    const historyData = await fetchHistory('temperature', 20);
    if (historyData.length > 0) {
        const labels = historyData.map(d => new Date(d.recorded_at).toLocaleTimeString('fr-FR'));
        const values = historyData.map(d => d.value);
        updateChart(labels, values);
    }
}
function updateChart(labels, values) {
    const ctx = document.getElementById('tempChart').getContext('2d');
    if (chart) chart.destroy();
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Température (°C)',
                data: values,
                borderColor: '#203a43',
                backgroundColor: 'rgba(32, 58, 67, 0.1)',
                tension: 0.3,
                pointRadius: 3
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: false } }
        }
    });
}

refreshBtn.addEventListener('click', updateDashboard);

updateDashboard();
setInterval(updateDashboard, 60000);