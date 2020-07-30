import requests
import json
import numpy

url_forwards = 'https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[%7B%22property%22:%22lastName%22,%22direction%22:%22ASC_CI%22%7D,%7B%22property%22:%22skaterFullName%22,%22direction%22:%22ASC_CI%22%7D]&start=100&limit=101&factCayenneExp=gamesPlayed%3E=30&cayenneExp=(positionCode=%22L%22%20or%20positionCode=%22R%22%20or%20positionCode=%22C%22)%20and%20active=1%20and%20gameTypeId=2%20and%20seasonId%3C=20192020%20and%20seasonId%3E=20102011'

records = requests.get(url_forwards).json()

players = records['data']

print("Count: ", len(players))
print(records['total'])

#for player in players:
#	print(player['goals'])
