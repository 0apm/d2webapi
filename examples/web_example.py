import os
import sys
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)
from config import STEAM_API_KEY

from src.d2webapi.d2webapi import Dota2API

#https://www.dota2.com/public/javascript/dota_react/main.js?v=W-YScytqFrR6&l=english&_cdn=cloudflare
#works also
#https://www.dota2.com/webapi/IDOTA2Fantasy/GetPlayerInfo/v001?account_id=96183976
# https://cdn.cloudflare.steamstatic.com/apps/dota2/players/96183976.png
def main():
    api = Dota2API(data_dir=root_path+'/dotaapi_cache', api_key=STEAM_API_KEY)
    #print(api.get_match_detail(7081579203))
    #print(api.get_league_matches(15137))
    #api.web_get_single_team_info(8894818) Ooredoo Thunders
    #api.get_team_info_by_teamid(8722443)
    #api.web_get_player_info(96183976) #TA2000
    #api.web_get_league_data(15199) # Pinnacle Cup: Malta Vibes #1
    #api.web_get_league_data(15137) # EEU DPC
    #api.web_get_DPC_standings(8) #spring season???
    api.get_event_portraits(15137)


if __name__ == "__main__":
   main()

