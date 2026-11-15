// System Load Auto-Refresh with Needle Gauges
let refreshInterval;

function fetchSystemLoad() {
    fetch('/api/system/load')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateGaugeDisplay(data);
        })
        .catch(error => {
            console.error('Error fetching system load:', error);
        });
}

function updateGaugeDisplay(data) {
    // Update CPU gauge
    if (data.cpu_usage !== undefined) {
        updateGauge('cpu', data.cpu_usage);
        updateWarningState('cpu', data.cpu_usage);
    }

    // Update RAM gauge
    if (data.ram_usage !== undefined) {
        updateGauge('ram', data.ram_usage);
        updateWarningState('ram', data.ram_usage);
    }

    // Update Temperature gauge
    if (data.cpu_temp !== undefined && data.cpu_temp !== null) {
        updateTempGauge(data.cpu_temp);
        updateWarningState('temp', data.cpu_temp, true);
    }
}

function updateGauge(type, value) {
    const needle = document.getElementById(`${type}-needle`);
    const valueEl = document.getElementById(`${type}-value`);
    
    if (needle && valueEl) {
        needle.style.setProperty('--percentage', value);
        valueEl.textContent = `${value.toFixed(1)}%`;
    }
}

function updateTempGauge(temp) {
    const needle = document.getElementById('temp-needle');
    const valueEl = document.getElementById('temp-value');
    
    if (needle && valueEl) {
        const percent = Math.min(temp, 80);
        needle.style.setProperty('--percentage', percent);
        valueEl.textContent = `${temp.toFixed(1)}°C`;
    }
}

function updateWarningState(type, value, isTemp = false) {
    const cards = document.querySelectorAll('.gauge-card');
    let card = null;
    
    if (type === 'cpu' && cards.length > 0) card = cards[0];
    else if (type === 'ram' && cards.length > 1) card = cards[1];
    else if (type === 'temp' && cards.length > 2) card = cards[2];
    
    if (!card) return;

    card.classList.remove('warning', 'danger');

    if (isTemp) {
        if (value > 70) {
            card.classList.add('danger');
        } else if (value > 55) {
            card.classList.add('warning');
        }
    } else {
        if (value > 80) {
            card.classList.add('danger');
        } else if (value > 60) {
            card.classList.add('warning');
        }
    }
}

// Initialize auto-refresh
function initSystemLoadRefresh(interval = 5000) {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
    fetchSystemLoad();
    refreshInterval = setInterval(fetchSystemLoad, interval);
}

document.addEventListener('DOMContentLoaded', function() {
    initSystemLoadRefresh();
});

window.addEventListener('beforeunload', function() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
});
