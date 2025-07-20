import os
from twilio.rest import Client

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_number = os.getenv('TWILIO_FROM_NUMBER')

client = Client(account_sid, auth_token)

def send_sms(to_number, message):
    client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    ) 