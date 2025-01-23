import googlemaps
from .models import Incident
from django.shortcuts import render
from .forms import IncidentForm
from .utils import is_within_university
from .tasks import send_incident_notification
from django.conf import settings


# Initialize Google Maps client with your API key -- THIS KEYCAN BE CHANGED TO SUIT AZURE MAPS||MAPBOX etc
gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

def save_incident(request):
    if request.method == "POST":
        form = IncidentForm(request.POST)
        if form.is_valid():
            # Get user input and live location data from form
            user = request.user
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            user_input_location = form.cleaned_data.get('user_input_location')

            live_location = None

            # Validate live location (from geolocation)
            if latitude and longitude:
                latitude = float(latitude)
                longitude = float(longitude)

                # Reverse geocode the live location to get its description
                reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
                if reverse_geocode_result:
                    live_location = reverse_geocode_result[0]['formatted_address']

                # Check if the live location is within the University of Ibadan boundary
                if not is_within_university(latitude, longitude):
                    form.add_error(None, "Live location is outside the University of Ibadan boundary.")
                    return render(request, 'incident_form.html', {'form': form})

            # Validate user input location (geocoding user input)
            if user_input_location:
                try:
                    # Geocode user input location to get latitude and longitude
                    geocode_result = gmaps.geocode(user_input_location)
                    if geocode_result:
                        input_lat = geocode_result[0]['geometry']['location']['lat']
                        input_lon = geocode_result[0]['geometry']['location']['lng']

                        # Check if the user input location is within the University of Ibadan boundary
                        if not is_within_university(input_lat, input_lon):
                            form.add_error('user_input_location', "The entered location is outside the University of Ibadan boundary.")
                            return render(request, 'incident_form.html', {'form': form})
                    else:
                        form.add_error('user_input_location', "Unable to geocode the entered location.")
                        return render(request, 'incident_form.html', {'form': form})

                except Exception as e:
                    form.add_error('user_input_location', f"Error with Google Maps API: {e}")
                    return render(request, 'incident_form.html', {'form': form})

            # If both locations are valid, save the incident
            incident = form.save(commit=False)
            incident.user = user
            incident.live_location = live_location  # Set live_location to the formatted address from reverse geocoding
            incident.save()

            # Send notification asynchronously (using Celery)
            send_incident_notification.delay(incident.incident_id)

            #Return the success response with the form
            return render(request, 'incident-form.html', {'form': form})

    else:
        form = IncidentForm()

    return render(request, 'incident-form.html', {'form': form})
