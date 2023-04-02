import json
import os
import sys
sys.path.append(os.path.join(sys.path[0], 'src'))

#from src.d2webapi.d2webapi import Dota2API
#from config import STEAM_API_KEY

def main():
    #api = Dota2API(api_key=STEAM_API_KEY)
    #print(api.get_match_detail(7081579203))
    #print(api.get_league_matches(15137))
    #api.get_team_info_by_teamid(8722443)
    #api.get_team_info_by_teamid(8722443)
    with open('dotaapi_cache/leagues.json') as f:
        data = json.load(f)
    print(len(data))
    unique_tiers = list(set(item['tier'] for item in data))
    print(unique_tiers)
#    newdata = sorted(data, key=lambda x: x['leagueid'])

#    with open('dotaapi_cache/leagues_sorted.json', 'w') as f:
#       json.dump(newdata, f)


if __name__ == "__main__":
   main()

