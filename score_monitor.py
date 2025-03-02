import time
import os
import requests
from message import format_message, send_message
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

SCORES_FEED = os.environ['LIVE_SCORES_API']


def main():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    print("Checking for updates")
    while True:
        init_response = requests.get(SCORES_FEED, headers=headers).json()
        timestamp = init_response['lastUpdated']['timestamp']
        time.sleep(30)
        response = requests.get(SCORES_FEED, headers=headers).json()
        check_timestamp = response['lastUpdated']['timestamp']
        if timestamp < check_timestamp:
            for item in response['items']:
                if item['event']['timestamp'] > timestamp:
                    message = format_message(item)
                    send_message(message)


if __name__ == "__main__":
    main()
