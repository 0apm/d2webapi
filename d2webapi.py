"""
My small python Wrapper for Steam Web API

Official Steam Web API Documentation: https://wiki.teamfortress.com/wiki/WebAPI

About
-----
"""
# The OpenDota class serves as a python interface for the original OpenDota API
# in the form of a thin wrapper. The class assumes some familiarity with the
# OpenDota API.

# All method calls return serializable python objects, as return by the API,
# in most cases a dict or a list. Response data is stored as JSON in a local
# directory (Default: ~/dota2), to prevent the load on OpenDota API.
"""
Features
--------

* Functions for the most frequently used API calls
* Ability to authenticate using API key
* In-built and cusomizable limit to protect against frequent API calls
* Local file-based storage for frequent requests (persistent cache)
"""
###############################################################################

from dataclasses import dataclass, field
import json
import logging
import os
import time
from typing import Any
import requests

###############################################################################

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

###############################################################################

DOTA_ID = 570
DOTA_PRIVATE_BETA = 816
DOTA_BETA_TEST = 205790
URL = 'https://api.steampowered.com/IDOTA2Match_{game_id}/{method}/v1'
URL_STATS = 'https://api.steampowered.com/IDOTA2MatchStats_{game_id}/{method}/v1'

###############################################################################

@dataclass
class Dota2API:
    data_dir: str = field(default=None)
    api_key: str = field(default=None, repr=False)
    delay: int = field(default=3, repr=False)
    #api_url: str = field(default=None, repr=False)

    def __post_init__(self):
        self._session = requests.Session()
        if self.api_key is None:
            raise ValueError('Value for Steam API key must be provided')

        if self.data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__import__("__main__").__file__)), "dotaapi_cache")
            #self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dotaapi_cache")
        os.makedirs(self.data_dir, exist_ok=True)
        LOGGER.info('Creating')
    
    # ----------------------------------------------------------------------- #

    def request(
        self,
        url: str,
        params: dict,
        *,  # learning - Знак * в данном случае используется для указания, 
            # что после него все последующие параметры должны быть заданы только с явным указанием их имени (keyword-only arguments)
        post: bool = False,
        data: dict = None,
        filename: str = None,
        force: bool = False
    ) -> Any:
        # получаем данные из файла, если они есть
        path = None
        if filename is not None:
            path = os.path.join(self.data_dir, filename)
            if not force and os.path.isfile(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        json_data = json.load(f)
                    LOGGER.info(
                        f"Loading previously fetched data from '{filename}'."
                    )
                    return json_data
                except Exception:
                    LOGGER.exception(
                        f"Unexpected exception while work with file '{filename}'."
                    )
        
        time.sleep(self.delay) # ожидаем, чтобы не превысить api limits

        LOGGER.info(f"Query URL: {url}")
        params_log = {k: v for k, v in params.items() if k != 'key'}
        LOGGER.info(f"Query Params: {params_log}")
        response = self._session.get(url, params=params)
        content = response.content.decode("utf-8")
        
        try:
            json_data = json.loads(content)
        except Exception as e:
            LOGGER.exception(
                f"Unexpected exception {e} while parsing JSON from '{url}'."
            )
            return None

        if 'error' in json_data.get('result'):
            LOGGER.warning(f"Could not fetch '{url}' ({json_data['result']['error']}).")
            return None

        if path is not None:
            try:
                with open(path, "w") as f:
                    json.dump(json_data, f, ensure_ascii=False)
            except (FileNotFoundError, PermissionError, TypeError) as e:
                LOGGER.exception(
                    f"Unexpected exception {e} while writing to file '{path}'."
                )
        return json_data

    def get_match_detail(self, match_id: int, force: bool = False):
        params = {
            'match_id': match_id,
            'key': self.api_key,
        }

        url = URL.format(game_id=DOTA_ID, method='GetMatchDetails')
        return self.request(url, params, filename=f'match_{match_id}.json', force=force)
        
    def get_league_matches(self, league_id: int, force: bool = False):
        params = {
            'league_id': league_id,
            'key': self.api_key,
            #'matches_requested': 100
        }

        url = URL.format(game_id=DOTA_ID, method='GetMatchHistory')
        return self.request(url, params, filename=f'league_{league_id}_matches.json', force=force)
    
