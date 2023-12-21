// Using Fetch API to send data to the view then display the result in the HTML page
var comparisonChart = null; // Global variable to hold the chart instance

document.addEventListener('DOMContentLoaded', function() {
    // Get form, URL, and chart containers
    const form = document.querySelector('#myForm');
    const url = form.dataset.url;
    const chartContainer = document.getElementById('chartContainer');

    // Add a submit event listener to the form
    form.addEventListener('submit', function(event) {
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

            // Show the chart container
            chartContainer.style.display = 'flex'; // Use 'flex' if you're using flexbox

            // Show the progress bar container and feature importance chart container
            document.getElementById('progressBarContainer').style.display = 'block';
            document.getElementById('importanceChartContainer').style.display = 'block';

            // Create the progress bar with the prediction percentage
            createProgressBarChart(percentage);
            
            // Update the comparative chart with new data
            createComparativeChart(formData, data.avg_positive, data.avg_negative);

            // Create the feature importance chart
            createFeatureImportanceChart(data.coefficients, data.feature_names);
        });
    });
});

function createProgressBarChart(percentage) {
    const ctx = document.getElementById('progressBarChart').getContext('2d');

    if (window.progressBarChart instanceof Chart) {
        window.progressBarChart.destroy(); // Destroy the old chart instance if it exists
    }

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
                            value: 70,
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
                            value: 20,
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
        label: 'Average for Heart Failure Positive Outcome',
        data: labels.map(label => avgPositive[label]),
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
    };
    const negativeDataSet = {
        label: 'Average for Hear Failure Negative Outcome',
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

function createFeatureImportanceChart(coefficients, featureNames) {
    console.log('Coefficients:', coefficients); // Log the coefficients
    console.log('Feature Names:', featureNames); // Log the feature names

    const ctx = document.getElementById('featureImportanceChart').getContext('2d'); // Ensure your canvas has this id

    if (window.featureImportanceChart instanceof Chart) {
        window.featureImportanceChart.destroy(); // Destroy the old chart instance if it exists
    }

    // Take the absolute value of the coefficients
    const absoluteCoefficients = coefficients.map(coef => Math.abs(coef));

    // Sort the features based on the absolute value of coefficients
    const sortedFeatures = featureNames
        .map((name, index) => ({ name, value: absoluteCoefficients[index] }))
        .sort((a, b) => b.value - a.value);

    const sortedCoefficients = sortedFeatures.map(feature => feature.value);
    const sortedFeatureNames = sortedFeatures.map(feature => feature.name);

    try {
        // Create the feature importance chart
        window.featureImportanceChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: sortedFeatureNames,
                datasets: [
                    {
                        label: 'Variable Importance',
                        data: sortedCoefficients,
                        backgroundColor: 'rgba(0, 123, 255, 0.5)',
                        borderColor: 'rgba(0, 123, 255, 1)',
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                indexAxis: 'y',
                scales: {
                    x: {
                        beginAtZero: true,
                    },
                },
                legend: {
                    display: true,
                },
                responsive: true,
                maintainAspectRatio: false,
            },
        });
    } catch (error) {
        console.error('Error creating feature importance chart:', error);
    }
}