import googlemaps
from .models import Incident
from django.shortcuts import render, redirect
from .forms import IncidentForm
from .utils import is_within_university, geocode, reverse_geocode,send_incident_notification
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Initialize Google Maps client with your API key
gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

def save_incident(request):
    if request.method == "POST":
        form = IncidentForm(request.POST)
        if form.is_valid():
            user = request.user
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            user_input_location = form.cleaned_data.get('user_input_location')

            live_location = None

            # Validate live location (from geolocation)
            if latitude and longitude:
                try:
                    latitude = float(latitude)
                    longitude = float(longitude)

                    # Reverse geocode the live location with Google Maps
                    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
                    live_location = reverse_geocode_result[0]['formatted_address'] if reverse_geocode_result else None
                    print(live_location)

                    if not is_within_university(latitude, longitude):
                        form.add_error(None, "Live location is outside the University of Ibadan boundary.")
                        return render(request, 'incident-form.html', {'form': form})
                except ValueError:
                    form.add_error(None, "Invalid location coordinates provided.")
                    return render(request, 'incident-form.html', {'form': form})

            # Validate user input location
            if user_input_location:
                try:
                    # Geocode the user input location with Google Maps
                    geocode_result = gmaps.geocode(user_input_location)
                    if geocode_result:
                        input_lat = geocode_result[0]['geometry']['location']['lat']
                        input_lon = geocode_result[0]['geometry']['location']['lng']
                        print(input_lat,input_lon)
                    else:
                        form.add_error('user_input_location', "Unable to geocode the entered location.")
                        return render(request, 'incident-form.html', {'form': form})

                    if not is_within_university(input_lat, input_lon):
                        form.add_error('user_input_location', "The entered location is outside the University of Ibadan boundary.")
                        return render(request, 'incident-form.html', {'form': form})

                except Exception as e:
                    form.add_error('user_input_location', f"Error with location lookup: {e}")
                    return render(request, 'incident-form.html', {'form': form})

            # Save incident if valid
            incident = form.save(user=request.user, commit=False)
            incident.user = user
            incident.live_location = live_location
            incident.save()

            # Send notification asynchronously
            send_incident_notification(incident.incident_id)

            return redirect('success')

    else:
        form = IncidentForm()

    return render(request, 'incident-form.html', {'form': form})

@login_required(login_url='login')
def incident_report_success(request):
    return render(request,'success.html')
