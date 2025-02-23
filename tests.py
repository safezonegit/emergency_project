from django.conf import settings
import requests

settings.configure()

termii_api_url = getattr(settings, "TERMII_API_URL", "https://v3.api.termii.com/api/sms/send")

TERMII_API_KEY="TLepwSomaoLYEQgrabKkMVkuBfAWNUakiFfWOLfjDfHuRHSbNKnfBwTDMZwwtR"
TERMII_SENDER_ID="Safezone"

def resp():
    payload = {
        "api_key": TERMII_API_KEY,
        "to": "+2349052916517",
        "from": TERMII_SENDER_ID,
        "sms": "test",
        "type": "plain",
        "channel": "generic"
    }
    try:
        response = requests.post(termii_api_url, json=payload, timeout=10)
        print (response.json())
        response.raise_for_status()
    except requests.HTTPError as exc:
        print("Response Status:", response.status_code)
        print("Response Body:", response.text)
    except Exception as exc:
        print("Unexpected error notifying responder %s: %s",exc)


resp()