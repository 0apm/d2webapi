import json
import os
import random
import time
import requests
import threading

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#/dotaapi_cache

def get_players_id_from_league(filename: str) -> list:
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            json_data = json.load(f)
            print('ok')
    except Exception:
        print('Failed while working with file')
    
    players_list = [x['account_id'] for x in json_data['registered_players']]
    return players_list
    


def download_image(id):
    url = f'https://cdn.cloudflare.steamstatic.com/apps/dota2/players/{id}.png'
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'images/player_{id}.png', 'wb') as f:
            f.write(response.content)
        print(f'Successfully downloaded image for player {id}')
    else:
        print(f'Failed to download image for player {id}, response code: {response.status_code}')


if __name__ == '__main__':
    if not os.path.exists('images'):
        os.makedirs('images')
    players_EEU = get_players_id_from_league(os.path.join(root_path, 'dotaapi_cache', 'web_leagues_15137.json'))
    pl = players_EEU[4:]
    for i in range(len(pl)):
        download_image(pl[i])
        time.sleep(random.randint(45, 60))