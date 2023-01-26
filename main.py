
from bs4 import BeautifulSoup
import os
import re
from datetime import datetime
import requests
from dotenv import load_dotenv
load_dotenv()

LIVE_SCORES_API = os.environ.get("LIVE_SCORES_API")
headers = {"User-Agent": "Mozilla/5.0"}


# Needed to remove text from day.
def fmt_date(s):
    return re.sub(r"(\d)(st|nd|rd|th)", r"\1", s)


# Function to get next fixture.
# Return dictionary with opponent and epoch date/time of next match
def get_next_fixtures(team="Queens Park Rangers"):
    print(f"Getting next fixtures for {team}")

    fixtures = requests.get(
        "https://www.qpr.co.uk/fixtures/first-team", headers=headers)
    soup = BeautifulSoup(fixtures.text, "html.parser")

    next_fixtures_section = soup.find("section", attrs={
        "class": "fixtures-banner"}).find("div", attrs={"class": "fixtures-banner__content"})

    opponent_a, opponent_b = next_fixtures_section.findAll("h3")
    opponent_a_date, opponent_b_date = next_fixtures_section.findAll("p")

    return {
        "next": {
            "date": int(datetime.timestamp(datetime.strptime(fmt_date(opponent_a_date.text.strip()), "%d %B %Y %H:%M %p"))),
            "opponent": opponent_a.text
        },
        "after": {
            "date": int(datetime.timestamp(datetime.strptime(fmt_date(opponent_b_date.text.strip()), "%d %B %Y %H:%M %p"))),
            "opponent": opponent_b.text
        }
    }


def game_on(current, next):
    if (current >= next and current < next + 7200):
        print("Game is being played")
        return True
    else:
        print("No game being played")


def main():
    current_time = int(datetime.now().timestamp())
    vidi = requests.get(LIVE_SCORES_API, headers=headers).json()
    vidiprinter_updated = vidi.get("lastUpdated")["timestamp"]
    fixtures = get_next_fixtures()
    if (game_on(current_time, fixtures["next"]["date"])):
        print("Hello world")
    else:
        print("No World?")


if __name__ == "__main__":
    main()
