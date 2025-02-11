document.getElementById('get-location').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent form submission

    // Show the custom prompt
    showLocationPrompt();
  });

  // Show the custom location prompt
  function showLocationPrompt() {
    document.getElementById('location-confirmation').style.display = 'block';
  }

  // When the user clicks 'Yes, Share Location'
  function confirmLocation() {
    document.getElementById('location-confirmation').style.display = 'none';

    // Now request the browser's location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(async function(position) {
        console.log("Location granted: ", position);

        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        document.getElementById('latitude').value = latitude;
        document.getElementById('longitude').value = longitude;

        // Show loading spinner while fetching address
        document.getElementById('loading-spinner').style.display = 'inline-block';

        try {
          // Fetch location using Google's Geolocation API
          const apiKey = "AIzaSyBtZQijM7JpE--1CM6SeTS3ylbZiFsn8to"; // Replace with your actual API key
          const response = await fetch(`https://www.googleapis.com/geolocation/v1/geolocate?key=${apiKey}`, {
            method: "POST",
          });

          const data = await response.json();

          if (data.location) {
            const latlng = { lat: latitude, lng: longitude };
            const geocoder = new google.maps.Geocoder();

            geocoder.geocode({ location: latlng, region: 'NG', language: 'en' }, function(results, status) {
              if (status === google.maps.GeocoderStatus.OK && results.length > 0) {
                let formattedAddress = null;

                for (let result of results) {
                  if (
                    !result.formatted_address.includes("+") &&
                    result.types.some(type => ["street_address", "route", "locality", "sublocality"].includes(type))
                  ) {
                    formattedAddress = result.formatted_address;
                    break;
                  }
                }

                formattedAddress = formattedAddress || results[0].formatted_address;
                document.getElementById('user_input_location').value = formattedAddress;
                alert("📍 Location detected: " + formattedAddress);
              } else {
                alert("❌ Could not fetch a valid address. Please try again.");
              }
            });
          } else {
            alert("❌ Unable to get location from Google API.");
          }
        } catch (error) {
          console.error(error);
          alert("❌ Error fetching location. Please check your connection or try again.");
        } finally {
          // Hide the spinner after the operation is complete
          document.getElementById('loading-spinner').style.display = 'none';
        }
      }, function(error) {
        console.error("Error obtaining location: ", error);
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