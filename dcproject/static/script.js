document.getElementById('startSimulationBtn').addEventListener('click', function() {
    // Show loading spinner
    document.getElementById('loadingSpinner').style.display = 'block';

    fetch('/start_simulation', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        const outputContainer = document.getElementById('outputContainer');
        outputContainer.innerHTML = '';  // Clear previous output
        data.forEach(message => {
            const messageElement = document.createElement('p');
            messageElement.textContent = message;
            outputContainer.appendChild(messageElement);
        });

        // Hide loading spinner after simulation ends
        document.getElementById('loadingSpinner').style.display = 'none';
    })
    .catch(error => {
        console.error('Error:', error);
        const outputContainer = document.getElementById('outputContainer');
        outputContainer.innerHTML = "<p>Error fetching simulation data.</p>";
        document.getElementById('loadingSpinner').style.display = 'none';  // Hide spinner on error
    });
});
