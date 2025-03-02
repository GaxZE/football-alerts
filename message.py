import os, requests, json
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)


CHAT_ID = os.environ['CHAT_ID']
BOT_TOKEN = os.environ['BOT_TOKEN']

def send_message(message):
    payload = {
        "text": "Required",
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": None
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?text={message}&chat_id={CHAT_ID}"
    requests.post(url, json=payload, headers=headers)


def format_message(data):
    """
    Format a message based on the football event type.

    Args:
        data (dict): Dictionary containing event and teams information.

    Returns:
        list: List of formatted message strings for the events.
    """
    messages = []

    for item in data.get("items", []):
        event = item.get("event", {})
        teams = item.get("teams", {})
        competition = item.get("competition", {}).get("name", {}).get("code", "Unknown League")
        minutes = event.get("minutes", "0:00")

        def get_team_info(side):
            team = teams.get(side, {})
            name = team.get("name", {}).get("short", f"Unknown {side.capitalize()} Team")
            score = team.get("score", 0)
            return name, score

        home_team, home_score = get_team_info("home")
        away_team, away_score = get_team_info("away")
        score_line = f"{home_score} - {away_score}"
        event_type = event.get("type")

        if event_type == 11:  # Goal
            team_id = event.get("teamId")
            team_name = home_team if team_id == 1 else away_team
            player = event.get("player", {}).get("name", {})
            player_name = f"{player.get("forename", "Unknown")} {player.get("surname", "Player")}".strip()
            info = event.get("info", "")
            messages = f"*GOAL*: {home_team} {score_line} {away_team}\n{player_name} {minutes}\n{info}"

        elif event_type == 5:  # Player sent off
            team_id = event.get("teamId")
            team_name = home_team if team_id == 1 else away_team
            player = event.get("player", {}).get("name", {})
            player_name = f"{player.get("forename", "Unknown")} {player.get("surname", "Player")}".strip()
            info = event.get("info", "").capitalize()
            messages = f"*OFF*: {player_name} ({team_name})\n{info} {minutes}"

        elif event_type in {6, 7}:  # Half-time or Full-time
            period = "HT" if event_type == 6 else "FT"
            messages = f"*{period}*: {home_team} {score_line} {away_team}\n{competition}"

        else:  # Unknown event
            messages = f"*EVENT* ({competition}) [{minutes}] {event}"

    return messages



# Load JSON file and parse it
with open("data/scores.json", "r") as file:
    data = json.load(file)  # Convert JSON to dictionary

# Call the function with the parsed JSON data
message = format_message(data)

# Print the result
print(f"{message}\n")
