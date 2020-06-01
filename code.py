import time
import pandas as pd
import numpy as np
from riotwatcher import LolWatcher, ApiError

pd.set_option('display.max_columns', 999)

# golbal variables
api_key = 'RGAPI-309c8acf-20f1-4a78-a9b3-6a8ad78ae911'
watcher = LolWatcher(api_key)
my_region = 'na1'
summoner_name = 'NotSoSrs'
my_id = watcher.summoner.by_name(my_region, summoner_name)
latest_version = watcher.data_dragon.versions_for_region(my_region)['n']['champion']

# Grab match details, ARAM only (queue==450)
matches_list = []
for x in range(1800,2000,100):
    time.sleep(1.3)
    matches = watcher.match.matchlist_by_account(my_region, my_id['accountId'], begin_time=0, begin_index=x, end_index=x+99,season=[13])
    for match in matches['matches']: #matches['matches'] is a list of dicts
        if match['queue'] == 450:
            match_attr = list(match.values())
            matches_list.append(match_attr)
matches_df = pd.DataFrame(matches_list,columns=match.keys())
# Grab participant champions and winning team
participants_list = []
winning_team_list = []
for index, row in matches_df.iterrows():
    time.sleep(1.3)
    match_details = watcher.match.by_id(my_region, row['gameId'])
    if match_details['teams'][0]['win'] == 'Win':
        winning_team_list.append('blue_win')
    else:
        winning_team_list.append('red_win')
    participants = []
    for x in range(0,10):
        participants.append(match_details['participants'][x]['championId'])
    participants_list.append(participants)
# Concat into one df
participants_columns = ['blue_1','blue_2','blue_3','blue_4','blue_5','red_1','red_2','red_3','red_4','red_5']
participants_df = pd.DataFrame(participants_list,columns=participants_columns)
winning_team_df = pd.DataFrame(winning_team_list,columns=['winning_team'])
df = pd.concat([matches_df, participants_df, winning_team_df], axis=1)

# Create champ id dictionary
static_champ_list = watcher.data_dragon.champions(latest_version, False, 'en_US')
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']
# Create champ role(s) dictionary
champ_dict_tags = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict_tags[row['key']] = row['tags']
# Convert champ num to name
for col in participants_columns:
    df[col] = df[col].astype('str')
    df[col + '_tags'] = df[col].map(champ_dict_tags).replace('[]','')
    df[col] = df[col].replace(champ_dict)
# Create my champ columns
df['champion'] = df['champion'].astype('str')
df['my_champion'] = df['champion'].map(champ_dict)
df['my_champion_tag'] = df['champion'].map(champ_dict_tags)
# Create win_or_lose columns
win_or_lose_list = []
for index, row in df.iterrows():
    if (row['my_champion'] in list(row[8:13])) & (row['winning_team']=='blue_win'):
        win_or_lose_list.append('W')
    elif (row['my_champion'] in list(row[8:13])) & (row['winning_team']=='red_win'):
        win_or_lose_list.append('L')
    elif (row['my_champion'] in list(row[14:19])) & (row['winning_team']=='blue_win'):
        win_or_lose_list.append('L')
    elif (row['my_champion'] in list(row[14:19])) & (row['winning_team']=='red_win'):
        win_or_lose_list.append('W')
win_or_lose_df = pd.DataFrame(win_or_lose_list, columns=['win_or_lose'])
df = pd.concat([df, win_or_lose_df], axis=1)
df.head()
