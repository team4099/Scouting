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

def get_team_score(team_key):
    team_number = int(team_key[3:])
    if team_number in data:
        elos = data[team_number]
        #x, y = zip(*enumerate(elos))
        #return poly.polyval(len(x) + 1, poly.polyfit(x, y, 1))
        div = 1
        div += len(elos) >= 2
        return sum(elos[-2:]) / div
    return -1

def get_average_auto_score(team_key):
    events = loads(requests.get(base_url + "team/" + team_key + "/2016/events", headers=headers).text)
    if events:
        total = 0
        count = 0
        for event in events:
            matches = loads(requests.get(base_url + "team/" + team_key + "/event/" + event["key"] + "/matches", headers=headers).text)
            for match in matches:
                if match["comp_level"] == "qm" and match["score_breakdown"]:
                    alliance = [alliance for alliance in match["alliances"] if team_key in match["alliances"][alliance]["teams"]][0]
                    total += match["score_breakdown"][alliance]["autoPoints"]
                    count += 1
        return total / count
    return -1

def get_penalties(team_key):
    events = loads(requests.get(base_url + "team/" + team_key + "/2016/events", headers=headers).text)
    if events:
        total = 0
        count = 0
        for event in events:
            matches = loads(requests.get(base_url + "team/" + team_key + "/event/" + event["key"] + "/matches", headers=headers).text)
            for match in matches:
                if match["comp_level"] == "qm" and match["score_breakdown"]:
                    alliance = [alliance for alliance in match["alliances"] if team_key in match["alliances"][alliance]["teams"]][0]
                    total += match["score_breakdown"][alliance]["foulCount"]
                    count += 1
        return total / count
    return -1

events = int(input("Number of events to stalk: "))

if events < 1:
    exit(0)

methods = (get_team_score, get_average_auto_score, get_penalties)
print("Select sort method ->")
print("\t1. Average team score for past two years")
print("\t2. Average autonomous score for 2016")
print("\t3. Average number of penalties for 2016")
method = methods[int(input("Option: ")) - 1]

event_id = input("Event ID #1 (including year): ")
event_info = loads(requests.get(base_url + "event/" + event_id + "/teams", headers=headers).text)
teams = []
keys = set()
for team_info in event_info:
    key = team_info["key"]
    keys.add(key)
    teams.append([method(key), team_info])

for event in range(2, events + 1):
    event_id = input("Event ID #" + str(event) + " (including year): ")
    event_info = loads(requests.get(base_url + "event/" + event_id + "/teams", headers=headers).text)
    for team_info in event_info:
        key = team_info["key"]
        if key not in keys:
            keys.add(key)
            teams.append([method(key), team_info])

for team in sorted(teams, key=lambda t: t[0], reverse = True):
    print("-" * 50)
    team_info = team[1]
    print(team_info["key"])
    print(team_info["name"] + " - " + str(team[0]))
    website = team_info["website"]
    if None != website != "http://www.firstinspires.org/":
        print(website)
