// Scripts for the contact form popup
function openSendingModal() {
    // Display the sending modal
    document.getElementById('sending-modal').style.display = 'block';
}

function closeSendingModal() {
    // Hide the sending modal
    document.getElementById('sending-modal').style.display = 'none';
}

function openModal() {
    // Display the success modal
    document.getElementById('success-modal').style.display = 'block';
}

function closeModal() {
    // Hide the success modal
    document.getElementById('success-modal').style.display = 'none';

    // Optional: Redirect the user or perform other actions after closing the modal
    // window.location.href = '/redirect-url';
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('contact-form').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Show the "sending..." modal
        openSendingModal();

        // Your AJAX request here
        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.getAttribute('action'),
            data: formData,
            success: function (data) {
                // Hide the "sending..." modal
                closeSendingModal();

                // Show the success modal
                openModal();
            },
            error: function (xhr, errmsg, err) {
                // Hide the "sending..." modal in case of an error
                closeSendingModal();

                // Handle errors if needed
                console.log(xhr.status + ": " + xhr.responseText);
            },
            processData: false,
            contentType: false,
        });
    });
});
