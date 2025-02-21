import googlemaps
from .models import Incident
from django.shortcuts import render, redirect
from .forms import IncidentForm
from .utils import is_within_university, geocode, reverse_geocode,send_incident_notification
from django.conf import settings
from django.contrib.auth.decorators import login_required
import re


# Initialize Google Maps client with your API key
gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

@login_required(login_url='login')
def save_incident(request):
    if request.method == "POST":
        form = IncidentForm(request.POST)
        if form.is_valid():
            user = request.user
            user_input_location = form.cleaned_data.get('user_input_location')

            # Clean up the location input:
            # Remove any instance of "universityofibadan" (with or without commas/spaces)
            if user_input_location:
                user_input_location = re.sub(r",?\s*University of Ibadan", "", user_input_location, flags=re.IGNORECASE).strip()
                # Now user_input_location should be something like "zik hall"
            else:
                form.add_error('user_input_location', "Please enter a location.")
                return render(request, 'incident-form.html', {'form': form})

            # Validate cleaned location via Google Maps geocoding
            try:
                geocode_result = gmaps.geocode(user_input_location)
                if geocode_result:
                    input_lat = geocode_result[0]['geometry']['location']['lat']
                    input_lon = geocode_result[0]['geometry']['location']['lng']
                    print("User location coordinates:", input_lat, input_lon)
                else:
                    form.add_error('user_input_location', "Unable to geocode the entered location.")
                    return render(request, 'incident-form.html', {'form': form})

                # Check if the geocoded coordinates are within the University boundary
                if not is_within_university(input_lat, input_lon):
                    form.add_error('user_input_location', "The entered location is outside the University of Ibadan boundary.")
                    return render(request, 'incident-form.html', {'form': form})

            except Exception as e:
                form.add_error('user_input_location', f"Error with location lookup: {e}")
                return render(request, 'incident-form.html', {'form': form})

            # Save incident if valid
            incident = form.save(user=request.user, commit=False)
            incident.user = user
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
