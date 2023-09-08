
# Data Imports
import requests
from bs4 import BeautifulSoup

#import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
import re


###   PITCHER STATS *** NEEDS WORK

def scrape_pitcher_stats(player_id):
    url = f"https://www.baseball-reference.com/players/gl.fcgi?id={player_id}&t=p&year=2023"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    pitcher_stats = []
    game_stats = {}
    pitching_gamelogs = soup.find_all('tr', id=lambda value: value and value.startswith('pitching_gamelogs.'))
    print(pitching_gamelogs[0])

    for i in range(len(pitching_gamelogs)):
        if i <= 15:  # Adjust the number of games as per your requirement
            
            game_stats = {
                'Date': pitching_gamelogs[-1-i].find('td', {'data-stat': 'date_game'}).get_text().replace('\xa0', ' '),
                'Opponent': pitching_gamelogs[-1-i].find('td', {'data-stat': 'team_ID'}).get_text(),
                'Result': pitching_gamelogs[-1-i].find('td', {'data-stat': 'game_result'}).get_text(),
                'Decision': pitching_gamelogs[-1-i].find('td', {'data-stat': 'player_game_result'}).get_text(),
                'IP': pitching_gamelogs[-1-i].find('td', {'data-stat': 'IP'}).get_text(),
                'H': pitching_gamelogs[-1-i].find('td', {'data-stat': 'H'}).get_text(),
                'R': pitching_gamelogs[-1-i].find('td', {'data-stat': 'R'}).get_text(),
                'ER': pitching_gamelogs[-1-i].find('td', {'data-stat': 'ER'}).get_text(),
                'BB': pitching_gamelogs[-1-i].find('td', {'data-stat': 'BB'}).get_text(),
                'SO': pitching_gamelogs[-1-i].find('td', {'data-stat': 'SO'}).get_text(),
                'HR': pitching_gamelogs[-1-i].find('td', {'data-stat': 'HR'}).get_text(),
                'HBP': pitching_gamelogs[-1-i].find('td', {'data-stat': 'HBP'}).get_text(),
                'ERA': pitching_gamelogs[-1-i].find('td', {'data-stat': 'earned_run_avg'}).get_text(),
                'Pitches': pitching_gamelogs[-1-i].find('td', {'data-stat': 'pitches'}).get_text(),
                'Strikes': pitching_gamelogs[-1-i].find('td', {'data-stat': 'strikes_total'}).get_text(),
            }
            print(game_stats)
            pitcher_stats.append(game_stats)

    game_stats = list(game_stats)  # Convert tuple to list\

    season_statsP = {
        'W/L': soup.find('tfoot').find('td', {'data-stat': 'player_game_result'}).text,
        'IP': soup.find('tfoot').find('td', {'data-stat': 'IP'}).text,
        'R': soup.find('tfoot').find('td', {'data-stat': 'R'}).text,
        'ER': soup.find('tfoot').find('td', {'data-stat': 'ER'}).text,
        'BB': soup.find('tfoot').find('td', {'data-stat': 'BB'}).text,
        'SO': soup.find('tfoot').find('td', {'data-stat': 'SO'}).text,
        'H': soup.find('tfoot').find('td', {'data-stat': 'H'}).text,
        'HR': soup.find('tfoot').find('td', {'data-stat': 'HR'}).text,
        'HBP': soup.find('tfoot').find('td', {'data-stat': 'HBP'}).text,
        'ERA': soup.find('tfoot').find('td', {'data-stat': 'earned_run_avg'}).text,
        'Strike %': soup.find('tfoot').find('td', {'data-stat': 'strikes_total'}).text,
        'WHIP': '{:.2f}'.format((Decimal(soup.find('tfoot').find('td', {'data-stat': 'BB'}).text) + Decimal(soup.find('tfoot').find('td', {'data-stat': 'H'}).text)) / Decimal(soup.find('tfoot').find('td', {'data-stat': 'IP'}).text)),
        'Opp BAA': '{:.3f}'.format((Decimal(soup.find('tfoot').find('td', {'data-stat': 'H'}).text) / Decimal(soup.find('tfoot').find('td', {'data-stat': 'AB'}).text)))
    }

    last_5_stats = calculate_pitcher_stats(pitcher_stats[:5])  # Summary statistics for last 5 games
    last_10_stats = calculate_pitcher_stats(pitcher_stats[:10])  # Summary statistics for last 10 games
    last_15_stats = calculate_pitcher_stats(pitcher_stats[:15])  # Summary statistics for last 15 games

    return {
        'game_stats': pitcher_stats,
        'last_5_stats': last_5_stats,
        'last_10_stats': last_10_stats,
        'last_15_stats': last_15_stats,
        'season_stats': season_statsP
    }

def calculate_pitcher_stats(pitcher_stats):
    total_stats = {
        'IP': 0.0,
        'R': 0,
        'ER': 0,
        'BB': 0,
        'SO': 0,
        'H': 0,
        'HR': 0,
        'HBP': 0,
        'ERA': 0.00,
        'Pitches': 0,
        'Strikes': 0,
        'WHIP': 0.00
    }

    for stats in pitcher_stats:
        for key in total_stats:
            if key == 'IP':
                value = str(stats.get(key, '0'))
                if value:
                    try:
                        total_stats[key] += '{:.1f}'.format(Decimal(value))
                    except Exception as e:
                        print(f"Error converting '{value}' to Decimal: {e}")

            elif key in ['ERA','WHIP']:
                continue
            else:
                total_stats[key] += int(stats.get(key, 0))

    if total_stats['IP'] > 0:
        total_stats['WHIP'] = (total_stats['H'] + total_stats['BB'])/ total_stats['IP']
        total_stats['WHIP'] = Decimal(total_stats['WHIP']).quantize(Decimal('.00'), rounding=ROUND_HALF_UP)

        total_stats['ERA'] = total_stats['ER']/total_stats['IP']
        total_stats['ERA'] = total_stats['ERA'].quantize(Decimal('.000'), rounding=ROUND_HALF_UP)

    return total_stats



###    HITTER STATS
def scrape_hitter_stats(player_id):
    url = f"https://www.baseball-reference.com/players/gl.fcgi?id={player_id}&t=b&year=2023"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    hitter_stats = []
    game_stats = {}
    batting_gamelogs = soup.find_all('tr', id=lambda value: value and value.startswith('batting_gamelogs.'))
    #print(batting_gamelogs[0])
    #
    for i in range(len(batting_gamelogs)):
        if i <= 30:  # Adjust the number of games as per your requirement

            game_stats = {
                'Date': batting_gamelogs[-1-i].find('td', {'data-stat': 'date_game'}).get_text(),
                'Opp': batting_gamelogs[-1-i].find('td', {'data-stat': 'opp_ID'}).get_text(),
                'Results': batting_gamelogs[-1-i].find('td', {'data-stat': 'game_result'}).get_text(),
                'AB': batting_gamelogs[-1-i].find('td', {'data-stat': 'AB'}).get_text(),
                'H': batting_gamelogs[-1-i].find('td', {'data-stat': 'H'}).get_text(),
                'BB': batting_gamelogs[-1-i].find('td', {'data-stat': 'BB'}).get_text(),
                'K': batting_gamelogs[-1-i].find('td', {'data-stat': 'SO'}).get_text(),
                'R': batting_gamelogs[-1-i].find('td', {'data-stat': 'R'}).get_text(),
                'RBI': batting_gamelogs[-1-i].find('td', {'data-stat': 'RBI'}).get_text(),
                'HR': batting_gamelogs[-1-i].find('td', {'data-stat': 'HR'}).get_text(),
                'SB': batting_gamelogs[-1-i].find('td', {'data-stat': 'SB'}).get_text(),
                'CS': batting_gamelogs[-1-i].find('td', {'data-stat': 'CS'}).get_text(),
                'BAA': batting_gamelogs[-1-i].find('td', {'data-stat': 'batting_avg'}).get_text(),
                'OBP': batting_gamelogs[-1-i].find('td', {'data-stat': 'onbase_perc'}).get_text(),
                'SLG': batting_gamelogs[-1-i].find('td', {'data-stat': 'slugging_perc'}).get_text(),
                'OPS': batting_gamelogs[-1-i].find('td', {'data-stat': 'onbase_plus_slugging'}).get_text(),
            }
            #print(game_stats)
            hitter_stats.append(game_stats)

    game_stats = list(game_stats)  # Convert tuple to list

    
    season_stats = {
        'AB': soup.find('tfoot').find('td', {'data-stat': 'AB'}).text,
        'H': soup.find('tfoot').find('td', {'data-stat': 'H'}).text,
        'BB': soup.find('tfoot').find('td', {'data-stat': 'BB'}).text,
        'K': soup.find('tfoot').find('td', {'data-stat': 'SO'}).text,
        'R': soup.find('tfoot').find('td', {'data-stat': 'R'}).text,
        'RBI': soup.find('tfoot').find('td', {'data-stat': 'RBI'}).text,
        'HR': soup.find('tfoot').find('td', {'data-stat': 'HR'}).text,
        'SB': soup.find('tfoot').find('td', {'data-stat': 'SB'}).text,
        'CS': soup.find('tfoot').find('td', {'data-stat': 'CS'}).text,
        'BAA': soup.find('tfoot').find('td', {'data-stat': 'batting_avg'}).text,
        'OBP': soup.find('tfoot').find('td', {'data-stat': 'onbase_perc'}).text,
        'SLG': soup.find('tfoot').find('td', {'data-stat': 'slugging_perc'}).text,
        'OPS': soup.find('tfoot').find('td', {'data-stat': 'onbase_plus_slugging'}).text,
    }

    last_10_stats = calculate_hitter_stats(hitter_stats[:10])  # Summary statistics for last 10 games
    #print(last_10_stats)
    last_20_stats = calculate_hitter_stats(hitter_stats[:20])  # Summary statistics for last 20 games
    last_30_stats = calculate_hitter_stats(hitter_stats[:30])  # Summary statistics for last 30 games

    return {
        'game_stats': hitter_stats,
        'last_10_stats': last_10_stats,
        'last_20_stats': last_20_stats,
        'last_30_stats': last_30_stats,
        'season_stats': season_stats
    }

def calculate_hitter_stats(hitter_stats):
    total_stats = {
        'AB': 0,
        'H': 0,
        'BB': 0,
        'K': 0,
        'R': 0,
        'RBI': 0,
        'HR': 0,
        'SB': 0,
        'CS': 0,
        'BAA': "{:.3f}".format(0)
    }

    for stats in hitter_stats:
        for key in total_stats:
            if key == 'BAA':
                continue
            else:
                total_stats[key] += int(stats.get(key, 0))
                #print(key, int(stats.get(key, 0)))

    if total_stats['AB'] > 0:
        total_stats['BAA'] = "{:.3f}".format(total_stats['H'] / total_stats['AB'])
        # total_stats['BAA'] = total_stats['BAA'].quantize(Decimal('.000'), rounding=ROUND_HALF_UP)

    return total_stats


###   PLAYER SEARCH

# Find players baseball-reference id and position
def find_player_id(player_name):
    # Get the first letter of the player's last name
    last_name_initial = player_name.split()[-1][0].lower()
    
    # Construct the URL for the players with the same last name initial
    url = f"https://www.baseball-reference.com/players/{last_name_initial}/"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the player link based on the player name
        player_link = soup.find("a", string=lambda s: s and player_name.lower() in s.lower())
        
        if player_link:
            # Extract the player ID from the href attribute
            href = player_link["href"]
            player_id = href.split("/")[3].split(".")[0]
            positions, stats_indicators = get_player_positions(player_id)
            
            
            return player_id, positions, stats_indicators
    
    # If the player ID is not found, return None
    return None, [], []

# Get player full name from player_id
def get_player_full_name(player_id):
    url = f"https://www.baseball-reference.com/players/{player_id[0]}/{player_id}.shtml"   
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title_tag = soup.find("title")

    if title_tag:
        full_name = title_tag.text.split("|")[0].strip()
        names = full_name.split("Stats")[0].strip().split()
        last_name = names[-1]
        
        if len(names) > 1:
            first_name = names[:-1]
            return f"{' '.join(first_name)} {last_name}"
        
        return last_name

    return ""

def get_player_positions(player_id):
    url = f"https://www.baseball-reference.com/players/{player_id[0]}/{player_id}.shtml"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the position element on the player's profile page
    position_element = soup.find('strong', string='Position:')
    
    # If not found, try finding the position element for 'Positions:'
    if position_element == None:
        position_element = soup.find('strong', string='Positions:')

    if position_element:
        positions_text = position_element.next_sibling.strip()
        positions = positions_text.split(' and ')
        stats_indicators = []
        
        for position in positions:
            if 'Pitcher' in position:
                stats_indicators.append('pitcher')
            else:
                stats_indicators.append('hitter')
        
        return positions_text, stats_indicators
    
    return [], []


if __name__ == '__main__':
    player = "Brayan Bello"
    playerID = find_player_id(player)
    print(playerID)

    if 'hitter' in playerID[2]:
        statsH = scrape_hitter_stats(playerID[0])
        print('Hitter Stats: ', statsH)
    
    if 'pitcher' in playerID[2]:
        statsP = scrape_pitcher_stats(playerID[0])
        print('Pitcher Stats: ', statsP)
    