// Station Météo — dashboard client

const METRICS = {
    temperature: { valueEl: 'temp-value',     timeEl: 'temp-time',     unit: '°C',   digits: 1 },
    humidity:    { valueEl: 'humidity-value', timeEl: 'humidity-time', unit: '%',    digits: 0 },
    windspeed:   { valueEl: 'wind-value',     timeEl: 'wind-time',     unit: 'km/h', digits: 1 },
    pressure:    { valueEl: 'pressure-value', timeEl: 'pressure-time', unit: 'hPa',  digits: 0 },
};

const syncDot = document.getElementById('sync-dot');
const syncText = document.getElementById('sync-text');
const refreshBtn = document.getElementById('refreshBtn');
let chart = null;

// Backend orders /measurements ascending, so the LAST row is the most recent.
async function fetchSeries(metric, limit = 200) {
    try {
        const res = await fetch(`/measurements?metric=${metric}&limit=${limit}`);
        if (!res.ok) return [];
        return await res.json();
    } catch (e) {
        console.warn(`Pas de données pour ${metric}`, e);
        return [];
    }
}

function setReadout(metric, series) {
    const cfg = METRICS[metric];
    const valueEl = document.getElementById(cfg.valueEl);
    const timeEl = document.getElementById(cfg.timeEl);
    if (!series.length) return;

    const latest = series[series.length - 1];
    valueEl.innerHTML =
        `${Number(latest.value).toFixed(cfg.digits)}<span class="unit">${cfg.unit}</span>`;
    timeEl.textContent =
        'relevé ' + new Date(latest.recorded_at).toLocaleString('fr-FR', {
            hour: '2-digit', minute: '2-digit', day: '2-digit', month: '2-digit'
        });
}

function markSync(ok) {
    syncDot.classList.toggle('live', ok);
    syncText.textContent = ok
        ? 'synchronisé ' + new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
        : 'aucune donnée';
}

async function updateDashboard() {
    const [temp, humidity, wind, pressure] = await Promise.all([
        fetchSeries('temperature'),
        fetchSeries('humidity'),
        fetchSeries('windspeed'),
        fetchSeries('pressure'),
    ]);

    setReadout('temperature', temp);
    setReadout('humidity', humidity);
    setReadout('windspeed', wind);
    setReadout('pressure', pressure);

    markSync(temp.length > 0);

    const recent = temp.slice(-24);
    if (recent.length) {
        updateChart(
            recent.map(d => new Date(d.recorded_at).toLocaleString('fr-FR', {
                hour: '2-digit', minute: '2-digit'
            })),
            recent.map(d => d.value)
        );
    }
}

function updateChart(labels, values) {
    const ctx = document.getElementById('tempChart').getContext('2d');
    const grad = ctx.createLinearGradient(0, 0, 0, 260);
    grad.addColorStop(0, 'rgba(232, 113, 43, 0.22)');
    grad.addColorStop(1, 'rgba(232, 113, 43, 0)');

    if (chart) {
        chart.data.labels = labels;
        chart.data.datasets[0].data = values;
        chart.update();
        return;
    }

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Température (°C)',
                data: values,
                borderColor: '#E8712B',
                backgroundColor: grad,
                borderWidth: 2,
                fill: true,
                tension: 0.35,
                pointRadius: 0,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: '#E8712B',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#0F2027',
                    padding: 10,
                    titleFont: { family: 'IBM Plex Mono' },
                    bodyFont: { family: 'IBM Plex Mono' },
                    callbacks: { label: c => ` ${c.parsed.y} °C` }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: '#8A9AA6', font: { family: 'IBM Plex Mono', size: 10 }, maxRotation: 0, autoSkipPadding: 16 }
                },
                y: {
                    grid: { color: '#EDF1F4' },
                    border: { display: false },
                    ticks: { color: '#8A9AA6', font: { family: 'IBM Plex Mono', size: 10 } }
                }
            }
        }
    });
}

refreshBtn.addEventListener('click', updateDashboard);
updateDashboard();
setInterval(updateDashboard, 60000);
