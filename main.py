import requests
from json import loads
import numpy.polynomial.polynomial as poly

headers = {
    "X-TBA-App-Id": "frc4099:sneaky-team-stalking:0.0.1"
}
base_url = "https://www.thebluealliance.com/api/v2/"
with open("average_elo.csv") as file:
    data = {}
    for line in file.readlines()[1:]:
        l = list(map(int, [_ for _ in line[:-4].split(",") if "0" != _ != ""]))
        data[l[0]] = l[1:]

def get_team_scores(team_key):
    if team_key in data:
        elos = data[team_key]
        x, y = zip(*enumerate(elos))
        return poly.polyval(len(x) + 1, poly.polyfit(x, y, 1))
        #if len(elos) >= 2:
        #    return sum(elos[-2:]) / 2
        #return sum(elos[-2:])
    else:
        return 0

events = int(input("Number of events to stalk: "))

if events < 1:
    exit(0)

event_id = input("Event ID #1 (including year): ") + "/"
event_info = loads(requests.get(base_url + "event/" + event_id + "teams", headers=headers).text)
teams = []
keys = set()
for team_info in event_info:
    key = team_info["key"]
    keys.add(key)
    teams.append([get_team_scores(int(key[3:])), team_info["name"], team_info["website"], key])

for event in range(2, events + 1):
    event_id = input("Event ID #" + str(event) + " (including year): ") + "/"
    event_info = loads(requests.get(base_url + "event/" + event_id + "teams", headers=headers).text)
    for team_info in event_info:
        key = team_info["key"]
        if key not in keys:
            keys.add(key)
            teams.append([get_team_scores(int(key[3:])), team_info["name"], team_info["website"], key])

for team in sorted(teams, key=lambda t: t[0], reverse = True):
    print(team[3])
    print(team[1] + " - " + str(team[0]))
    if None != team[2] != "http://www.firstinspires.org/":
        print(team[2])
    print("-" * 50)
