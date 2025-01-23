from django.conf import settings
from twilio.rest import Client
from celery import shared_task
from .models import Incident
from responder.models import SecurityResponder, FireHazardResponder, MedicalResponder

@shared_task
def send_incident_notification(incident_id):
    try:
        incident = Incident.objects.get(id=incident_id)
        responders = []

        # Determine responders based on category
        if incident.category == 'medical':
            responders = MedicalResponder.objects.all()
        elif incident.category == 'fire':
            responders = FireHazardResponder.objects.all()
        elif incident.category == 'security':
            responders = SecurityResponder.objects.all()

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        for responder in responders:
            message = (
                f"Incident Alert!\n"
                f"Category: {incident.category}\n"
                f"Severity: {incident.severity}\n"
                f"Location: {incident.user_input_location or incident.live_location}\n"
                f"Reported By: {incident.user.username}"
            )
            try:
                client.messages.create(
                    to=responder.sms_contact,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    body=message
                )
            except Exception as e:
                print(f"Failed to notify responder {responder.name}: {e}")
    except Incident.DoesNotExist:
        print("Incident not found.")
