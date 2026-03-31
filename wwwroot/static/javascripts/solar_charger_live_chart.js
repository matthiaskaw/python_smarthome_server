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

async function updateChart(chart, dataField, data, dataset_index) {
    try {
        

        if (!data || data.length === 0) {
            console.error('No data received');
            return;
        }

        const labels = data.map(item => formatDate(item.DateTime));
        const temperatures = data.map(item => item[dataField]);

        if (!window.voltage_chart) {
            console.error('Chart is not initialized');
            return;
        }

        chart.data.labels = labels;
        chart.data.datasets[dataset_index].data = temperatures;
        chart.update();
    } catch (error) {
        console.error('Error updating chart:', error);
    }
}

async function fetchData() {
        try {
            const response = await fetch('/api/solar_charger_data');
            
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
    keys = data[1]
    ctx_voltage_arr = document.getElementById('voltage_chart');
     
    if (!ctx_voltage_arr) {
    console.error('Canvas element for temperature not found');
        return;
    }
    const colors = [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 206, 86)',
        'rgb(75, 192, 192)',
        'rgb(153, 102, 255)',
        'rgb(255, 159, 64)'
    ];

    let datasets = [];

    for (let i = 0; i < 6; i++) {
        datasets.push({
            label: keys[i],
            data: [],
            borderColor: colors[i],
            tension: 0.1
        });
    }
    voltageChart_arr = new Chart(ctx_voltage_arr, {
        type: 'line',
        data: {
            labels: [],
            datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x:{
                        title:{
                            display: true,
                            text: 'Day time'
                        }
                    },
                    y: {
                        min: 0,
                        max: 15,
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Voltage (V)'  // 👈 Y-Achsenbeschriftung
                        }
                    
                    }
                }
            }
        });
        

    


    async function updateAllCharts(){

        const data = await fetchData();

        keys = data[1]
        values = data[0]
        console.info(keys)

        for(let i = 0; i < keys.length; i++){

            let moduleVoltage_list = values.map(item => item[keys[i]]);
            let moduleVoltage = moduleVoltage_list.map(number => number.toFixed(2));
      
            document.getElementById(keys[i]).textContent = moduleVoltage[moduleVoltage.length-1] + " V"
            document.getElementById('voltage_chart').textContent = moduleVoltage + " V"
            window.voltageChart_arr = voltageChart_arr;
            
            updateChart(window.voltageChart_arr, keys[i], values, i);
        }
        
    }

    updateAllCharts();
    setInterval(updateAllCharts, 3000);

});
