import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import io
import sys

# Redirect output
buffer = io.StringIO()
sys.stdout = buffer

# Get today's date
date_today = datetime.today().strftime('%Y-%m-%d')

URL = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&sportId=51&sportId=21&startDate={date_today}&endDate={date_today}&timeZone=America/New_York&gameType=E&&gameType=S&&gameType=R&&gameType=F&&gameType=D&&gameType=L&&gameType=W&&gameType=A&&gameType=C&language=en&leagueId=104&&leagueId=103&&leagueId=160&&leagueId=590&hydrate=team,linescore(matchup,runners),xrefId,story,flags,statusFlags,broadcasts(all),venue(location),decisions,person,probablePitcher,stats,game(content(media(epg),summary),tickets),seriesStatus(useOverride=true)&sortBy=gameDate,gameStatus,gameType"
page = requests.get(URL)
# print(type(page.json())) # json stuff
data = page.json()
print(f"Scores for {date_today}:\n")
try:
    for i in range(len(data['dates'][0]['games'])):
        # temp = data['dates'][0]['games'][i]
        # print(list(temp.keys()))
        try:
            score = data['dates'][0]['games'][i]['linescore']['teams']
            home_score = score['home']['runs']
            away_score = score['away']['runs']
        except KeyError:
            pass
        teams = data['dates'][0]['games'][i]['teams']
        home_team = teams['home']['team']['clubName']
        away_team = teams['away']['team']['clubName']
        # soup = BeautifulSoup(page.content, "html.parser")
        # scores["Game" + str(i+1)] = dict()
        print(f"{away_team}: {away_score}, {home_team}: {home_score}")

    # Resetting output to regular way
    sys.stdout = sys.__stdout__
    # Catch output
    output = buffer.getvalue()
    buffer.close()
    # Email credentials
    sender_email = "derek.m.wang2@gmail.com"
    sender_password = "yjnl jrpn pteq ayoo"
    receiver_email = "derek.m.wang2@gmail.com"

    # Send up email skeleton
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Python Webscraper Baseball Scores"

    # Send redirected output
    message.attach(MIMEText(output, 'plain'))
    try:
        # Connect to Gmail server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Change format
        text = message.as_string()
        server.send_message(message)

    except Exception as e:
        print(f"Failed to send email {e}")

    finally:
        server.quit()


except IndexError:
    print("No games today!")



