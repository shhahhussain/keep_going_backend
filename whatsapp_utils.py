import os
import requests

base_url = 'https://graph.facebook.com/v19.0/'
phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

def send_whatsapp_message(to_number, message_body):
    url = f'{base_url}{phone_number_id}/messages'
    data = {
        'messaging_product': 'whatsapp',
        'to': to_number,
        'type': 'text',
        'text': {'body': message_body}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json() 