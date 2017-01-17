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

event_id = input("Event ID #1 (including year): ") + "/"
event_info = loads(requests.get(base_url + "events/" + event_id + "teams", headers=headers).text)
teams = []
keys = {}
for team_info in event_info:
    key = team["key"]
    keys.add(key)

event_id = input("Event ID #1 (including year): ")
event_info = loads(requests.get(base_url + event_id + "/teams", headers=headers).text)
for team_info in event_info:
    key = team["key"]
    
