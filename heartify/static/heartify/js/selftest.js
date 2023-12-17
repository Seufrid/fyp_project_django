// Using Fetch API to send data to the view then display the result in the HTML page
document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('#myForm');
    var url = form.dataset.url;

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        var formData = new FormData(this);

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.querySelector('#result').textContent = '';
            var percentage = (data.result * 100).toFixed(0);
            document.querySelector('#result').textContent += "Heart Failure Chance= " + percentage + '%';
        });
    });
});