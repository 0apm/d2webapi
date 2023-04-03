import json
import os
import sys
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)
from config import STEAM_API_KEY
import datetime

from src.d2webapi.d2webapi import Dota2API

def extract_nodes(node_groups):
    nodes = []
    for node_group in node_groups:
        if "nodes" in node_group:
            nodes += node_group["nodes"]
        if "node_groups" in node_group:
            nodes += extract_nodes(node_group["node_groups"])
    return nodes

def make_results(api, nodes, league_id):
    print(len(nodes))
    with open(api.data_dir+f'/nodes_{league_id}.json', "w", encoding="utf-8") as f:
        json.dump(nodes, f, ensure_ascii=False)
    
    try:
        with open(api.data_dir+f'/nodes_{league_id}_results.json', "w", encoding="utf-8") as f:
            for series in nodes:
                try:
                    if series["team_id_1"] and series["team_id_2"]:
                        team1 = api.web_get_single_team_info(series["team_id_1"])
                        team2 = api.web_get_single_team_info(series["team_id_2"])
                        f.write(f'series between: {team1["name"]} and {team2["name"]}\n')
                        f.write(f'at date: {datetime.datetime.fromtimestamp(series["scheduled_time"])}, actual time: {datetime.datetime.fromtimestamp(series["actual_time"])}\n')
                        f.write(f'result: {series["team_1_wins"]}:{series["team_2_wins"]}\n')
                        f.write('\n')
                    else:
                        f.write(f'Empty node {series["node_id"]}\n')
                except (TypeError, ValueError) as e:
                    f.write(f'Error with node {series["node_id"]}\n')
    except Exception as e:
        print('Unexpected file error', e)


def main():
    api = Dota2API(data_dir=root_path+'/dotaapi_cache', api_key=STEAM_API_KEY)
    league_data = api.web_get_league_data(15088) #
    node_groups = league_data["node_groups"]
    nodes = extract_nodes(node_groups)
    print(len(nodes)) # 28 = verno
    make_results(api, nodes, 15088)

if __name__ == "__main__":
   main()

