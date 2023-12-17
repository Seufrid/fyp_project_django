// Appointment page popup script
document.getElementById('appointmentForm').addEventListener('submit', function (event) {
    event.preventDefault();

    // Show loading modal
    $('#loadingModal').modal('show');

    var formData = new FormData(this);

    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            // Hide loading modal
            $('#loadingModal').modal('hide');

            if (data.status === 'success') {
                // Show success modal
                $('#successModal').modal('show');
            } else {
                // Show error modal
                $('#errorModal').modal('show');
                console.error(data.errors);
            }
        },
        error: function () {
            // Hide loading modal
            $('#loadingModal').modal('hide');

            // Show error modal
            $('#errorModal').modal('show');
        }
        
    });
});

function closeErrorModal() {
    // Hide loading modal
    $('#loadingModal').modal('hide');
    // Hide error modal
    $('#errorModal').modal('hide');
}

function closeSuccessModal() {
    // Hide loading modal
    $('#loadingModal').modal('hide');
    // Hide success modal
    $('#successModal').modal('hide');
}