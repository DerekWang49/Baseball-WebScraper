import requests
from bs4 import BeautifulSoup
from datetime import datetime
date_today = datetime.today().strftime('%Y-%m-%d')
URL = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&sportId=51&sportId=21&startDate={date_today}&endDate={date_today}&timeZone=America/New_York&gameType=E&&gameType=S&&gameType=R&&gameType=F&&gameType=D&&gameType=L&&gameType=W&&gameType=A&&gameType=C&language=en&leagueId=104&&leagueId=103&&leagueId=160&&leagueId=590&hydrate=team,linescore(matchup,runners),xrefId,story,flags,statusFlags,broadcasts(all),venue(location),decisions,person,probablePitcher,stats,game(content(media(epg),summary),tickets),seriesStatus(useOverride=true)&sortBy=gameDate,gameStatus,gameType"
page = requests.get(URL)
print(type(page.json())) # json stuff
data = page.json()
print("Current scores:")
try:
    for i in range(len(data['dates'][0]['games'])):
        score = data['dates'][0]['games'][i]['linescore']['teams']
        try:
            home_score = score['home']['runs']
            away_score = score['away']['runs']
        except KeyError:
            break
    teams = data['dates'][0]['games'][i]['teams']
    home_team = teams['home']['team']['clubName']
    away_team = teams['away']['team']['clubName']
    # soup = BeautifulSoup(page.content, "html.parser")
    print(f"{away_team}: {away_score}, {home_team}: {home_score}")
except IndexError:
    print("No games today!")


