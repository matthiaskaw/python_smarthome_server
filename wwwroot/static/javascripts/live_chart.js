function formatDate(dateString) {
        const date = new Date(dateString);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');

        //return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        return `${hours}:${minutes}`;
    }

async function updateChart(chart, dataField) {
    try {
        const data = await fetchData();
        if (!data || data.length === 0) {
            console.error('No data received');
            return;
        }

        const labels = data.map(item => formatDate(item.DateTime));
        const temperatures = data.map(item => item[dataField]);

        if (!window.tempChart) {
            console.error('Chart is not initialized');
            return;
        }

        chart.data.labels = labels;
        chart.data.datasets[0].data = temperatures;
        chart.update();
    } catch (error) {
        console.error('Error updating chart:', error);
    }
}


async function fetchData() {
        try {
            const response = await fetch('/api/data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            //console.log('Fetched data:', data); // Debug the fetched data
            return data;
        } catch (error) {
            console.error('Error fetching data:', error);
            return [];
        }
    }

document.addEventListener('DOMContentLoaded', function() {
    const ctx_temperature = document.getElementById('tempChart');
    const ctx_humidity = document.getElementById('humidChart');

    if (!ctx_temperature) {
        console.error('Canvas element not found');
        return;
    }
    
    const tempChart = new Chart(ctx_temperature, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temperature',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const humidChart = new Chart(ctx_humidity, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Humidity',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Make tempChart accessible globally
    window.tempChart = tempChart;
    window.humidChart = humidChart;
    


    // Initial data fetch and chart update
    async function updateAllCharts(){
        updateChart(window.tempChart, "Temperature");
        updateChart(window.humidChart, "Humidity");
    }
    // Update the chart every 5 seconds
    setInterval(updateAllCharts, 500);
});