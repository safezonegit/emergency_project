document.getElementById('get-location').addEventListener('click', function(event) {
  event.preventDefault(); // Prevent form submission
  showLocationPrompt();
});

// Display the custom location prompt UI.
function showLocationPrompt() {
  document.getElementById('location-confirmation').style.display = 'block';
}

// When the user clicks 'Yes, Share Location'
function confirmLocation() {
  document.getElementById('location-confirmation').style.display = 'none';

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      console.log("Location granted: ", position);

      // Extract coordinates from the browser's API.
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;

      // Update hidden fields with coordinates.
      document.getElementById('latitude').value = latitude;
      document.getElementById('longitude').value = longitude;

      // Show a loading spinner while fetching the address.
      document.getElementById('loading-spinner').style.display = 'inline-block';

      // Use Google Maps Geocoder to convert coordinates to a human-readable address.
      const latlng = { lat: latitude, lng: longitude };
      const geocoder = new google.maps.Geocoder();
      geocoder.geocode({ location: latlng, region: 'NG', language: 'en' }, function(results, status) {
        // Hide the spinner once done.
        document.getElementById('loading-spinner').style.display = 'none';
        
        if (status === google.maps.GeocoderStatus.OK && results.length > 0) {
          // Default to the first result.
          let formattedAddress = results[0].formatted_address;
          
          // Optionally, select a result with preferred address types.
          for (let result of results) {
            if (result.types.some(type => ["street_address", "route", "locality", "sublocality"].includes(type))) {
              formattedAddress = result.formatted_address;
              break;
            }
          }
          // Update the location input with the detected address.
          document.getElementById('user_input_location').value = formattedAddress;
          alert("📍 Location detected: " + formattedAddress);
        } else {
          alert("❌ Could not fetch a valid address. Please try again.");
        }
      });
    }, function(error) {
      console.error("Error obtaining location: ", error);
      alert("❌ Error obtaining your location. Please try again.");
    });
  } else {
    alert("Geolocation is not supported by this browser.");
  }
}

// When the user clicks 'No, I prefer not to'
function denyLocation() {
  document.getElementById('location-confirmation').style.display = 'none';
  alert("You have denied access to your location.");
}
