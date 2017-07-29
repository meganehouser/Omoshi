var ctx = document.getElementById('myChart').getContext('2d');
var chartOptions = {
    responsive: true,
    scales: {
        yAxes: [{
            id: "y-axis-1",
            position: "left",
            ticks: {
                max: 100,
                min: 0,
                stepSize: 10
            },
        }, {
            id: "y-axis-2",
            position: "right",
            ticks: {
                max: 50,
                min: 0,
                stepSize: 10
            },
        }],
    }
};

var chartData = {
    labels: label_data,
    datasets: [{
        type: 'line',
        label: '重さ',
        data: weight_data,
        backgroundColor: "rgba(152,255,41,0.4)",
        yAxisID: "y-axis-1",
        spanGaps: true,
    },{
        type: 'line',
        label: '体脂肪率',
        data: bodyfat_data,
        backgroundColor: "rgba(255,154,9,0.4)",
        yAxisID: "y-axis-2",
        spanGaps: true,
    }]
};
            
var myChart = new Chart(ctx,{ type: 'bar', data: chartData, options: chartOptions});
