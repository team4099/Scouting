import requests
from json import loads
import numpy # for later :O

headers = {
    "X-TBA-App-Id": "frc4099:sneaky-team-stalking:0.0.1"
}

base_url = "https://www.thebluealliance.com/api/v2/"

def get_team_history(team_key):
    # TODO
    pass

events = int(input("Number of events to stalk: "))

if events < 1:
    exit(0)

event_id = input("Event ID #1 (including year): ") + "/"
event_info = loads(requests.get(base_url + "events/" + event_id + "teams", headers=headers).text)
teams = []
keys = {}
for team_info in event_info:
    key = team["key"]
    keys.add(key)
    teams.append(get_team_history(key))

for event in range(2, events + 1):
    event_id = input("Event ID #" + str(event) + " (including year): ")
    event_info = loads(requests.get(base_url + "events/" + event_id + "teams", headers=headers).text)
    for team_info in event_info:
        key = team["key"]
        if key in keys:
            keys.add(key)
            teams.append(get_team_history(key))

