# Data Imports
import requests
from bs4 import BeautifulSoup

#import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
import re


def identifyTeamKs()
    url = f"https://www.baseball-reference.com/players/gl.fcgi?id={player_id}&t=b&year=2023"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    hitter_stats = []
    batting_gamelogs = soup.find_all('tr', id=lambda value: value and value.startswith('batting_gamelogs.'))