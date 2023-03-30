from d2webapi import Dota2API
from config import STEAM_API_KEY

def main():
    api = Dota2API(api_key=STEAM_API_KEY)
    print(api.get_match_detail(7081579203))
    print(api.get_league_matches(15137))

if __name__ == "__main__":
   main()