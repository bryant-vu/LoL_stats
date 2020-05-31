import time
import pandas as pd
import numpy as np
from riotwatcher import LolWatcher, ApiError

# golbal variables
api_key = 'RGAPI-e62df2ef-0274-4692-993d-00b68b145b79'
watcher = LolWatcher(api_key)
my_region = 'na1'
summoner_name = 'NotSoSrs'
me = watcher.summoner.by_name(my_region, summoner_name)

# Grab match details, ARAM only (queue==450)
matches_list = []
for x in range(0,2000,100):
    time.sleep(1.5)
    matches = watcher.match.matchlist_by_account(my_region, me['accountId'], begin_time=0, begin_index=x, end_index=x+99,season=[13])
    for match in matches['matches']: #matches['matches'] is a list of dicts
        if match['queue'] == 450:
            match_attr = list(match.values())
            matches_list.append(match_attr)
matches_df = pd.DataFrame(matches_list,columns=match.keys())
# win or loss

# playing x  hero


# Grab participant champions
participants_list = []
for index, row in matches_df.iterrows():
    time.sleep(1.5)
    match_details = watcher.match.by_id(my_region, row['gameId'])
    participants = []
    for x in range(0,10):
        participants.append(match_details['participants'][x]['championId'])
    participants_list.append(participants)

participants_columns = ['blue_1','blue_2','blue_3','blue_4','blue_5','red_1','red_2','red_3','red_4','red_5']
participants_df = pd.DataFrame(participants_list,columns=participants_columns)

# Concat match details with participant details
df = pd.concat([matches_df, participants_df], axis=1)

# Check league's latest version
latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
# Champ info
static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']

champ_dict_tags = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict_tags[row['key']] = row['tags']


for col in participants_columns:
    df[col] = df[col].astype('str')
    df[col + '_tags'] = df[col].map(champ_dict_tags).replace('[]','')
    df[col] = df[col].replace(champ_dict)

df.head()
