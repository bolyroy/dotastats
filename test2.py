#base code: https://github.com/AsTimeGoesBy111/Spotify-Music-Data-Analysis/blob/gh-pages/Code/Spotify_Extract_API_Data.py
#steam API documentation: https://wiki.teamfortress.com/wiki/WebAPI
#jsonmerge documentation: https://pypi.org/project/jsonmerge/
#lines 29-30: https://stackoverflow.com/questions/33955225/remove-duplicate-json-objects-from-list-in-python/3js3955336

import requests
import json
import copy
import objectpath
from jsonmerge import merge
from jsonmerge import Merger
import times
import sys
import lxml.etree as etree
import io
import os.path
from functools import reduce
import itertools
import docopt

#key, account_id, and steamids are all tied to my personal account
key = 'INPUT PERSONAL STEAM KEY'
account_id = '76561089'
p_steamid = '76561198036826817'

def main():
    API_recall(key,account_id)

# https://www.electricmonk.nl/log/2017/05/07/merging-two-python-dictionaries-by-deep-updating/
def deepupdate(target, src):
    for k, v in src.items():
        if type(v) == list:
            if not k in target:
                target[k] = copy.deepcopy(v)
            else:
                target[k].extend(v)
        elif type(v) == dict:
            if not k in target:
                target[k] = copy.deepcopy(v)
            else:
                deepupdate(target[k], v)
        elif type(v) == set:
            if not k in target:
                target[k] = v.copy()
            else:
                target[k].update(v.copy())
        else:
#            target[k] = copy.copy(v)
            pass

def API_recall(key,account_id):
    url_0 = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key='+key+'&account_id='+account_id+'&game_mode=1'
    fdict_obj = requests.get(url_0).json()
    fdict_str = json.dumps(fdict_obj)
    flastid = fdict_obj['result']['matches'][-1]['match_id']
    print(flastid)

    while True:
        try:
            url_1 = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key='+key+'&account_id='+account_id+'&game_mode=1&start_at_match_id='+str(flastid-1)
            ndict_obj = requests.get(url_1).json()
            ndict_str = json.dumps(ndict_obj)
            nlastid = ndict_obj['result']['matches'][-1]['match_id']

        except IndexError:
            break
            
        deepupdate(fdict_obj,ndict_obj)

        fdict_str = json.dumps(fdict_obj)
        flastid = fdict_obj['result']['matches'][-1]['match_id']
        print(flastid)

        if(flastid != nlastid):
            break
        continue

    with open('full call.json','w') as outfile:
        json.dump(fdict_obj,outfile,skipkeys=True,indent='\t')
    print('File save successful')
"""
    url = "https://api.opendota.com/api/players/"+account_id+"/matches"
    opdict_list = requests.get(url).json()
    opdict_str = json.dumps(opdict_list)
    opdict_obj = {d.pop("game_mode"): d for d in opdict_list}
    print (opdict_obj)

    deepupdate(fdict_obj,opdict_obj)
"""

def friends_define(key,p_steamid):
    list_url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v1/?key='+key+'&steamid='+p_steamid
    list_r = requests.get(list_url)
    #use list_r.json() to call all friends' IDs, get nicknames
    
    list_r.root
    
    steamids = []

    user_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+key+'&steamids='+steamids
    user_r = requests.get(user_url)

main()
