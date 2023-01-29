import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()


def send_telegram_message(message: str,
                          chat_id: str,
                          api_key: str):

    headers = {'Content-Type': 'application/json',
               'Proxy-Authorization': 'Basic base64'}
    data_dict = {'chat_id': chat_id,
                 'text': message,
                 'parse_mode': 'HTML',
                 'disable_notification': True}
    data = json.dumps(data_dict)
    url = f'https://api.telegram.org/bot{api_key}/sendMessage'
    response = requests.post(url,
                             data=data,
                             headers=headers,
                             verify=False)
    return response
