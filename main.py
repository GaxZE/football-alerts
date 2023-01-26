
from bs4 import BeautifulSoup
import os
import requests
from dotenv import load_dotenv
load_dotenv()

LIVE_SCORES_API = os.environ.get("LIVE_SCORES_API")


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
    print({next_opposition_team, next_opposition_date})


def main():
    get_next_fixture()


if __name__ == "__main__":
    main()
