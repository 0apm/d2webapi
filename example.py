from src.d2webapi.d2webapi import Dota2API
from config import STEAM_API_KEY

def main():
    api = Dota2API(api_key=STEAM_API_KEY)
    #print(api.get_match_detail(7081579203))
    #print(api.get_league_matches(15137))
    api.get_team_info_by_teamid(8722443)
    api.get_team_info_by_teamid(8722443)


if __name__ == "__main__":
   main()

