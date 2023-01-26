
from bs4 import BeautifulSoup
import os
import re
from datetime import datetime
import requests
from dotenv import load_dotenv
load_dotenv()

LIVE_SCORES_API = os.environ.get("LIVE_SCORES_API")


# Needed to remove text from day.
def fmt_date(s):
    return re.sub(r'(\d)(st|nd|rd|th)', r'\1', s)


# Function to get next fixture.
# Return dictionary with opponent and epoch date/time of next match
def get_next_fixture(team="Queens Park Rangers"):
    print(f"Getting next fixture for {team}")

    headers = {'User-Agent': 'Mozilla/5.0'}
    fixtures = requests.get(
        "https://www.qpr.co.uk/fixtures/first-team", headers=headers)
    soup = BeautifulSoup(fixtures.text, 'html.parser')

    next_fixture_section = soup.find("section", attrs={
        "class": "fixtures-banner"}).find("section", attrs={"class": "gamePromo"})

    next_opposition_team = next_fixture_section.find("h3").text.strip()
    next_opposition_date = next_fixture_section.find("p").text.strip()
    return {"date": int(datetime.timestamp(datetime.strptime(fmt_date(next_opposition_date), '%d %B %Y %H:%M %p'))), "opponent": next_opposition_team}


def main():
    next_match = get_next_fixture()
    print(next_match["opponent"])


if __name__ == "__main__":
    main()
