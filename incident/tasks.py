import logging
import requests
from celery import shared_task
from django.conf import settings
from .models import Incident
from responder.models import MedicalResponder, FireHazardResponder, SecurityResponder

logger = logging.getLogger(__name__)

@shared_task
def send_incident_notification(incident_id):
    """
    Sends an SMS notification about an incident to all relevant responders via Termii.
    """
    try:
        incident = Incident.objects.get(id=incident_id)
    except Incident.DoesNotExist:
        logger.error("Incident with id %s not found.", incident_id)
        return

    # Select responders based on incident category
    if incident.category == 'medical':
        responders = MedicalResponder.objects.all()
    elif incident.category == 'fire':
        responders = FireHazardResponder.objects.all()
    elif incident.category == 'security':
        responders = SecurityResponder.objects.all()
    else:
        logger.error("Unknown incident category: %s", incident.category)
        return

    # Construct the SMS message
    message = (
        f"Incident Alert!\n"
        f"Category: {incident.category}\n"
        f"Severity: {incident.severity}\n"
        f"Location: {incident.user_input_location or incident.live_location}\n"
        f"Reported By: {incident.user.username}"
    )

    # Termii API configuration from Django settings
    termii_api_url = getattr(settings, "TERMII_API_URL", "https://api.termii.com/api/sms/send")
    termii_api_key = settings.TERMII_API_KEY
    termii_sender_id = settings.TERMII_SENDER_ID

    # Send notification to each responder
    for responder in responders:
        payload = {
            "api_key": termii_api_key,
            "to": responder.sms_contact,  
            "from": termii_sender_id,
            "sms": message,
            "type": "plain",
            "channel": "generic"
        }
        try:
            response = requests.post(termii_api_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Notification sent to %s. Response: %s", responder.name, response.json())
        except requests.HTTPError as exc:
            logger.error("Failed to notify responder %s: %s", responder.name, exc)
        except Exception as exc:
            logger.error("Unexpected error notifying responder %s: %s", responder.name, exc)
