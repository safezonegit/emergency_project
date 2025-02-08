from django import forms
from .models import Incident

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = '__all__'  # Include all fields
        exclude = ['incident_id', 'live_location', 'user', 'location','incident_date','date_reported','status']  # Exclude specific fields

    def save(self, user, latitude=None, longitude=None, commit=True):
        # Create or update an `Incident` instance
        incident = super().save(commit=False)  # Get the unsaved instance
        incident.user = user  # Assign the user
        if commit:
            incident.save()  # Save to the database
        return incident
