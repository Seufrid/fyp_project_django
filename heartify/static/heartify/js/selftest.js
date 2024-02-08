// Global variables to hold chart instances
let comparisonChart = null;
let featureImportanceChart = null;
let progressBarChart = null;
let scatterChart = null;

document.addEventListener('DOMContentLoaded', function () {
    // Initialize form and URL
    const form = document.querySelector('#myForm');
    const url = form.dataset.url;

    // Add event listener for form submission
    form.addEventListener('submit', function (event) {
        event.preventDefault();  // Prevent default form submission

        // Fetch form data
        const formData = new FormData(this);

        // Post request to server
        fetch(url, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data, formData);
        });
    });
});

function displayResults(data, formData) {
    // Display the Heart Failure Chance percentage
    const percentage = (data.result * 100).toFixed(0);
    document.querySelector('#result').textContent = `Heart Failure Chance = ${percentage}%`;

    // Show chart containers
    document.getElementById('progressBarContainer').style.display = 'block';
    document.getElementById('comparisonChartContainer').style.display = 'block';
    document.getElementById('featureImportanceChartContainer').style.display = 'block';
    document.getElementById('scatterChartContainer').style.display = 'block';

    // Update charts with new data
    createProgressBarChart(percentage);
    createComparativeChart(formData, data.avg_positive, data.avg_negative);
    createFeatureImportanceChart(data.feature_importance);
    createScatterPlot(data.new_point, data.pca_class_0, data.pca_class_1, data.decision_boundary);
}

function createProgressBarChart(percentage) {
    const ctx = document.getElementById('progressBarChart').getContext('2d');

    // Destroy the old chart instance if it exists
    if (progressBarChart instanceof Chart) {
        progressBarChart.destroy();
    }

    // Create a new progress bar chart
    progressBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Heart Failure Risk'],
            datasets: [
                {
                    label: 'Risk Percentage',
                    data: [percentage],
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                },
            ],
        },
        options: {
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                },
            },
            plugins: {
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            mode: 'vertical',
                            scaleID: 'x',
                            value: 50,
                            borderColor: 'red',
                            borderWidth: 2,
                            label: {
                                enabled: true,
                                content: 'Dangerous Level',
                                position: 'center',
                                backgroundColor: 'rgba(255, 99, 132, 0.8)',
                            },
                        },
                        line2: {
                            type: 'line',
                            mode: 'vertical',
                            scaleID: 'x',
                            value: 10,
                            borderColor: 'green',
                            borderWidth: 2,
                            label: {
                                enabled: true,
                                content: 'Safe Level',
                                position: 'center',
                                backgroundColor: 'rgba(75, 192, 192, 0.8)',
                            },
                        },
                    },
                },
            },
            legend: {
                display: false,
            },
            responsive: true,
            maintainAspectRatio: false,
        },
    });
}

function createComparativeChart(userInput, avgPositive, avgNegative) {
    const ctx = document.getElementById('myComparisonChart').getContext('2d');

    // Destroy the old chart instance if it exists
    if (comparisonChart instanceof Chart) {
        comparisonChart.destroy();
    }

    // Transform user input into a format suitable for Chart.js
    const userValues = {};
    userInput.forEach((value, key) => {
        // Convert all values to float for uniformity
        userValues[key] = parseFloat(value);
    });

    // Exclude encoded categorical features
    const excludedFeatures = ['ChestPainType', 'RestingECG', 'ExerciseAngina', 'STSlope', 'Sex', 'FastingBS', 'Oldpeak'];
    const labels = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR'];
    const userDataSet = {
        label: 'Your Input',
        data: labels.map(label => userValues[label]),
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
    };
    const positiveDataSet = {
        label: 'Average for Heart Failure Positive',
        data: labels.map(label => avgPositive[label]),
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
    };
    const negativeDataSet = {
        label: 'Average for Heart Failure Negative',
        data: labels.map(label => avgNegative[label]),
        backgroundColor: 'rgba(153, 102, 255, 0.5)',
    };

    // Create a new comparative chart
    comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels.filter(label => !excludedFeatures.includes(label)), // Filter out the excluded features
            datasets: [userDataSet, positiveDataSet, negativeDataSet],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
}

function createFeatureImportanceChart(featureImportanceData) {
    const ctx = document.getElementById('featureImportanceChart').getContext('2d');

    // Destroy the old chart instance if it exists
    if (featureImportanceChart instanceof Chart) {
        featureImportanceChart.destroy();
    }

    // Transform the object into an array of [key, value] pairs and sort it by value in descending order
    const sortedData = Object.entries(featureImportanceData).sort((a, b) => b[1] - a[1]);

    // Split the sorted array into separate arrays for labels and data
    const labels = sortedData.map(item => item[0]);
    const dataValues = sortedData.map(item => item[1]);
    
    // Create a feature importance chart
    featureImportanceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Input Importance',
                data: dataValues,
                backgroundColor: 'rgba(0, 123, 255, 0.5)',
                borderColor: 'rgba(0, 123, 255, 1)',
                borderWidth: 1,
            }]
        },
        options: {
            indexAxis: 'y', // Set horizontal bar chart
            scales: {
                x: {
                    beginAtZero: true,
                }
            },
            responsive: true,
            maintainAspectRatio: false,
        }
    });
}

function createScatterPlot(newPoint, pcaData0, pcaData1, decisionBoundary) {
    const ctx = document.getElementById('scatterChart').getContext('2d');

    // Destroy the old chart instance if it exists
    if (scatterChart instanceof Chart) {
        scatterChart.destroy();
    }

    // Prepare the data for the chart
    var formattedData0 = pcaData0.map(function(item) {
        return { x: item.PCA_Component_1, y: item.PCA_Component_2 };
    });

    var formattedData1 = pcaData1.map(function(item) {
        return { x: item.PCA_Component_1, y: item.PCA_Component_2 };
    });

    // Create a scatter chart
    scatterChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Normal',
                data: formattedData0,
                backgroundColor: 'rgba(0, 0, 255, 0.5)'  
            }, {
                label: 'Heart Failure',
                data: formattedData1,
                backgroundColor: 'rgba(255, 0, 0, 0.5)' 
            }, {
                label: 'Your Data',
                data: [newPoint],
                backgroundColor: 'rgba(0, 255, 0, 0.5)' 
            }, {
                label: 'Boundary',
                data: decisionBoundary,
                backgroundColor: 'rgba(255, 0, 0, 0.1)', 
                showLine: true,  
                fill: false
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            }
        }
    });
}