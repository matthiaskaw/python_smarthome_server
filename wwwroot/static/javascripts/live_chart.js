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

async function updateChart(chart, dataField, sensor_name, data) {
    try {
        

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
        chart.label=sensor_name;
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
            return data;
        } catch (error) {
            console.error('Error fetching data:', error);
            return [];
        }
    }


document.addEventListener('DOMContentLoaded', async function() {


    const data = await fetchData();
    const groups = Object.keys(data);
    
    const ctx_humidity_arr = new Array();
    const ctx_temperature_arr = new Array();
    const ctx_voltage_arr = new Array();

    const tempChart_arr = new Array();
    const humidChart_arr = new Array();
    const voltageChart_arr = new Array();

    for(let i = 0; i < groups.length; i++) {
        
        ctx_temperature_arr[i] = document.getElementById('tempChart_'+groups[i]);
        ctx_humidity_arr[i] = document.getElementById('humidChart_'+groups[i]);
        ctx_voltage_arr[i] = document.getElementById('moduleVoltageChart_'+groups[i]);

        if (!ctx_temperature_arr[i]) {
            console.error('Canvas element for temperature not found');
            return;
        }
        

        if (!ctx_humidity_arr[i]) {
            console.error('Canvas element for humidity not found');
            return;
        }

        if(!ctx_voltage_arr[i]){
            console.error('Canvas element for voltage not found');
            return;
        }
        tempChart_arr[i] = new Chart(ctx_temperature_arr[i], {
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
        

        humidChart_arr[i] = new Chart(ctx_humidity_arr[i], {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Humidity',
                    data: [],
                    borderColor: 'rgb(192, 75, 75)',
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

        voltageChart_arr[i] = new Chart(ctx_voltage_arr[i], {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Module Voltage',
                    data: [],
                    borderColor: 'rgb(75, 192, 95)',
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
    }


    async function updateAllCharts(){

        const data = await fetchData();
        const groups = Object.keys(data);


        for(let i = 0; i < groups.length; i++){

            let moduleVoltage_list = data[groups[i]].map(item => item["ModuleVoltage"]);
            let moduleVoltage = moduleVoltage_list[moduleVoltage_list.length -1].toFixed(2);

            console.info(Number(moduleVoltage));
            document.getElementById('currentModuleVoltage_'+groups[i]).textContent = moduleVoltage + " V"
            window.tempChart = tempChart_arr[i];
            window.humidChart = humidChart_arr[i];
            window.voltageChart = voltageChart_arr[i];
            updateChart(window.tempChart, "Temperature", groups[i], data[groups[i]]);
            updateChart(window.humidChart, "Humidity", groups[i], data[groups[i]]);
            updateChart(window.voltageChart, "ModuleVoltage", groups[i], data[groups[i]]);

        }
    }

    updateAllCharts();
    setInterval(updateAllCharts, 1000);

});
