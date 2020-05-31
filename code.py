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

matches_list = []
for x in range(0,1999,100):
    matches = watcher.match.matchlist_by_account(my_region, me['accountId'], begin_time=0, begin_index=x, end_index=x+99,season=[13])
    for match in matches['matches']: #matches['matches'] is a list of dicts
        match_attr = list(match.values())
        matches_list.append(match_attr)
matches_df = pd.DataFrame(matches_list,columns=match.keys())

len(matches_df)

participants_list = []
for index, row in matches_df.iterrows():
    time.sleep(1.2)
    match_details = watcher.match.by_id(my_region, row['gameId'])
    participants = []
    for x in range(0,9):
        participants.append(match_details['participants'][x]['championId'])
    participants_list.append(participants)
participants_df = pd.DataFrame(participants_list,columns=['blue_1','blue_2','blue_3','blue_4','blue_5','red_1','red_2','red_3','red_4','red_5'])
len(participants_df)

#champions = watcher.data_dragon.champions('10.10.3216176')
