import pandas as pd
import numpy as np
from riotwatcher import LolWatcher, ApiError

# golbal variables
api_key = 'RGAPI-a1453a89-b310-46ef-9f36-1b7d3086aad4'
watcher = LolWatcher(api_key)
my_region = 'na1'
summoner_name = 'NotSoSrs'

me = watcher.summoner.by_name(my_region, summoner_name)

matches_df = pd.DataFrame()
for x in range(0,99,100):
    matches = watcher.match.matchlist_by_account(my_region, me['accountId'], begin_time=0, begin_index=x, end_index=x+99,season=[13])
    for match_attr in matches['matches']: #this is a list
        match_attr_list = match_attr.values()
        matches_df = matches_df.append(pd.Series(match_attr_list),ignore_index=True)
matches_df.columns = match_attr.keys()

print(matches_df.columns)

#champions = watcher.data_dragon.champions('10.10.3216176')
