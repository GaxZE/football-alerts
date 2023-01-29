
from bs4 import BeautifulSoup
import os
import re
import time
import json
from datetime import datetime
import requests
from notify import send_telegram_message
from dotenv import load_dotenv
load_dotenv()

LIVE_SCORES_API = os.environ.get("LIVE_SCORES_API")
headers = {"User-Agent": "Mozilla/5.0"}


# Needed to remove text from day.
def fmt_date(s: str):
    return re.sub(r"(\d)(st|nd|rd|th)", r"\1", s)


# Function to get next fixture.
# Return dictionary with opponent and epoch date/time of next match
def get_next_fixtures(team: str):
    fixtures = requests.get(
        "https://www.qpr.co.uk/fixtures/first-team", headers=headers)
    soup = BeautifulSoup(fixtures.text, "html.parser")

    next_fixtures_section = soup.find("section", attrs={
        "class": "fixtures-banner"}).find("div", attrs={"class": "fixtures-banner__content"})

    opponent_a, opponent_b = next_fixtures_section.findAll("h3")
    opponent_a_date, opponent_b_date = next_fixtures_section.findAll("p")

    return {
        "next": {
            "date": datetime.timestamp(datetime.strptime(fmt_date(opponent_a_date.text.strip()), "%d %B %Y %H:%M %p")),
            "opponent": opponent_a.text
        },
        "after": {
            "date": datetime.timestamp(datetime.strptime(fmt_date(opponent_b_date.text.strip()), "%d %B %Y %H:%M %p")),
            "opponent": opponent_b.text
        }
    }


def game_on(current: float, next: float):
    if (current >= next and current < next + 7200):
        print("Game is being played")
        return True
    else:
        print("No game being played")
        return False


def format_message(item: object):
    score = item["teams"]["home"]["name"]["full"] + " " + str(item["teams"]["home"]["score"]) + \
        "-" + str(item["teams"]["away"]["score"]) + " " +  \
        item["teams"]["away"]["name"]["full"]
    if (item["event"]["type"] == 1):
        goal_time = item["event"]["minutes"]
        info = item["event"]["info"]
        scorer = item["event"]["player"]["name"]["forename"] + \
            " " + item["event"]["player"]["name"]["surname"]
        send_message(f"GOAL: {score}")
        send_message(f"{scorer}({goal_time}) - {info})")
    elif (item["event"]["type"] == 6):
        send_message(f"HT: {score}")
    elif (item["event"]["type"] == 7):
        send_message(f"FT: {score}")


def send_message(message: str):
    send_telegram_message(message, os.environ.get(
        "CHAT_ID"), os.environ.get("BOT_TOKEN"))


def event_check(team: str, response: object, time: int):
    for item in response["items"]:
        if (item["teams"]["home"]["name"]["full"] == team or item["teams"]["away"]["name"]["full"] == team):
            if (item["event"]["timestamp"] > time):
                format_message(item)


def main():
    end = time.time() + 3600
    while True:
        print("Fetching updates...")
        live_scores = requests.get(LIVE_SCORES_API, headers=headers)
        parse_scores = json.loads(live_scores.text)
        init_check = parse_scores["lastUpdated"]["timestamp"]
        if time.time() > end:
            break
        time.sleep(30)
        live_scores_updated = requests.get(
            LIVE_SCORES_API, headers=headers)
        parse_scores_updated = json.loads(live_scores_updated.text)
        check_for_updates = parse_scores_updated["lastUpdated"][
            "timestamp"]
        if (init_check < check_for_updates):
            event_check("QPR", parse_scores_updated, init_check)
        else:
            print("No Updates")


if __name__ == "__main__":
    main()
