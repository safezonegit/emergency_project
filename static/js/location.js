document.getElementById('get-location').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent form submission when clicking "Get My Location"

    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                // Update the hidden fields in the form
                document.getElementById('latitude').value = latitude;
                document.getElementById('longitude').value = longitude;

                alert("Location fetched and added to the form!");
            },
            function (error) {
                if (error.code === error.PERMISSION_DENIED) {
                    alert("Location access denied. Please allow location access.");
                } else {
                    alert("An error occurred while retrieving your location.");
                }
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    } else {
        alert("Geolocation is not supported by your browser.");
    }
});
