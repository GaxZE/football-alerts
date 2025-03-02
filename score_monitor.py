import time
import os
import requests
import logging
from message import format_message, send_message
from dotenv import load_dotenv

# Load environment variables
load_dotenv(verbose=True, override=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SCORES_FEED = os.getenv("LIVE_SCORES_API")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/39.0.2171.95 Safari/537.36"
    )
}


def fetch_scores():
    """Fetch live scores data from the API with error handling."""
    try:
        response = requests.get(SCORES_FEED, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching scores: {e}")
        return None


def main():
    logging.info("Starting live scores checker...")
    initial_data = fetch_scores()
    if not initial_data:
        logging.error("Failed to retrieve initial data. Exiting.")
        return

    last_timestamp = initial_data.get("lastUpdated", {}).get("timestamp", 0)

    try:
        while True:
            time.sleep(30)
            data = fetch_scores()
            if not data:
                continue

            new_timestamp = data.get("lastUpdated", {}).get("timestamp", 0)
            if last_timestamp < new_timestamp:
                for item in data.get("items", []):
                    if item["event"]["timestamp"] > last_timestamp:
                        message = format_message(item)
                        send_message(message)
                last_timestamp = new_timestamp
    except KeyboardInterrupt:
        logging.info("Live scores checker stopped.")


if __name__ == "__main__":
    main()
