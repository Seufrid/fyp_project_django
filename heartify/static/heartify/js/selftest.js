// Global variable to hold the chart instance
let comparisonChart = null;

document.addEventListener('DOMContentLoaded', function () {
    // Get form, URL, and chart containers
    const form = document.querySelector('#myForm');
    const url = form.dataset.url;

    // Add a submit event listener to the form
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Get form data
        const formData = new FormData(this);

        // Send a POST request with form data to the specified URL
        fetch(url, {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                // Clear the result element
                const resultElement = document.querySelector('#result');
                resultElement.textContent = '';

                // Calculate and display the Heart Failure Chance percentage
                const percentage = (data.result * 100).toFixed(0);
                resultElement.textContent = `Heart Failure Chance = ${percentage}%`;

                // Show the progress bar container and feature importance chart container
                document.getElementById('progressBarContainer').style.display = 'block';
                document.getElementById('chartContainer').style.display = 'block';
                document.getElementById('featureImportanceChartContainer').style.display = 'block';

                // Create the progress bar with the prediction percentage
                createProgressBarChart(percentage);

                // Update the comparative chart with new data
                createComparativeChart(formData, data.avg_positive, data.avg_negative);

                // Create the feature importance chart
                createFeatureImportanceChart(data.feature_importance);
            });
    });
});

function createProgressBarChart(percentage) {
    const ctx = document.getElementById('progressBarChart').getContext('2d');

    // Destroy the old chart instance if it exists
    if (window.progressBarChart instanceof Chart) {
        window.progressBarChart.destroy();
    }

    // Create a new progress bar chart
    window.progressBarChart = new Chart(ctx, {
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
    // Destroy the existing chart instance if it exists
    if (comparisonChart) {
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

    const ctx = document.getElementById('myComparisonChart').getContext('2d');
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
    // Transform the object into an array of [key, value] pairs and sort it by value in descending order
    const sortedData = Object.entries(featureImportanceData).sort((a, b) => b[1] - a[1]);

    // Split the sorted array into separate arrays for labels and data
    const labels = sortedData.map(item => item[0]);
    const dataValues = sortedData.map(item => item[1]);

    // Get the context of the canvas element we want to select
    const ctx = document.getElementById('featureImportanceChart').getContext('2d');

    // Data for the chart
    const data = {
        labels: labels,
        datasets: [{
            label: 'Input Importance',
            data: dataValues,
            backgroundColor: 'rgba(0, 123, 255, 0.5)',
            borderColor: 'rgba(0, 123, 255, 1)',
            borderWidth: 1,
        }]
    };

    // Configuration of the chart
    const config = {
        type: 'bar',
        data: data,
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
    };

    // Create the chart
    new Chart(ctx, config);
}
