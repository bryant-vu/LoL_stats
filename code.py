import pandas as pd
import numpy as np
from riotwatcher import LolWatcher, ApiError

# golbal variables
api_key = 'RGAPI-a1453a89-b310-46ef-9f36-1b7d3086aad4'
watcher = LolWatcher(api_key)
my_region = 'na1'

me = watcher.summoner.by_name(my_region, 'NotSoSrs')
print(me)

my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])

# fetch last match detail
last_match = my_matches['matches'][0]
match_detail = watcher.match.by_id(my_region, last_match['gameId'])

last_match
participants = []

# check league's latest version
latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
# Lets get some champions static information
static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

# champ static list data to dict for looking up
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']
for row in participants:
    print(str(row['champion']) + ' ' + champ_dict[str(row['champion'])])
    row['championName'] = champ_dict[str(row['champion'])]

# print dataframe
df = pd.DataFrame(participants)
df
