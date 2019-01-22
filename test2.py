import json
from json.decoder import JSONDecodeError
import requests
import copy

#key, account_id, and steamids are all tied to my personal account
key = 'insert personal Steam Key'
account_id = '76561089'
p_steamid = '76561198036826817'

hero_id = 3

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

def heropool(key):
    url_0 = 'https://api.steampowered.com/IEconDOTA2_570/GetHeroes/V1/?key='+key+'&itemizedonly=true'
    hero_dict = requests.get(url_0).json()
    hero_r = hero_dict['result']['heroes']

    global hero_id
    hero_id = hero_r[-1]['id']
    print('Highest hero ID found is: ' + str(hero_id))
    print(str(hero_id) + ' operations expected to be performed.')

    try:
        with open('heroes.json','w') as outfile:
            json.dump(hero_r,outfile,skipkeys=True,indent='\t')
    except FileNotFoundError:
        pass
    print('Hero listing created successfully.')
    input('Press Enter to continue. . . ')

def API_recall_2(key,account_id):
    url_0 = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key='+key+'&account_id='+account_id+'&hero_id=1'
    fdict_obj = requests.get(url_0).json()
    fdict_str = json.dumps(fdict_obj)
    print(1)

    for x in range(2, hero_id):
        url_1 = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key='+key+'&account_id='+account_id+'&hero_id='+str(x)
        ndict_obj = requests.get(url_1).json()
        ndict_str = json.dumps(ndict_obj)

        deepupdate(fdict_obj,ndict_obj)
        print(x)
        x = x+1

        if x == hero_id:
            break

    print (str(x)+' concatenations performed successfully.')
    input('Press Enter to continue. . . ')

    url = "https://api.opendota.com/api/players/"+account_id+"/matches"
    opdict_list = requests.get(url).json()
    opdict_str = json.dumps(opdict_list)

    opdict_ref = {}
    for i in opdict_list:
        opdict_ref[i['match_id']] = i

    results = fdict_obj['result']['matches']
    for d in results:
        try:
            id = d['match_id']
            merge = opdict_ref[id]
            for k,v in merge.items():
                d[k] = v
            print(id)

        except KeyError:
            continue
    
    try:
        with open('full call2.json','w') as outfile:
            json.dump(fdict_obj,outfile,skipkeys=True,indent='\t')
    except FileNotFoundError:
        pass
    print('File save successful.')
    input('Press Enter to exit the program. . . ')

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

    print('Pull from Steam API was successful.')
    input('Press Enter to continue. . . ')

    url = "https://api.opendota.com/api/players/"+account_id+"/matches"
    opdict_list = requests.get(url).json()
    opdict_str = json.dumps(opdict_list)

    opdict_ref = {}
    for i in opdict_list:
        opdict_ref[i['match_id']] = i

    results = fdict_obj['result']['matches']
    for d in results:
        try:
            id = d['match_id']
            merge = opdict_ref[id]
            for k,v in merge.items():
                d[k] = v
            print(id)

        except KeyError:
            continue
    try:
        with open('full call.json','w') as outfile:
            json.dump(fdict_obj,outfile,skipkeys=True,indent='\t')
    except FileNotFoundError:
        pass
    print('File save successful.')
    input('Press Enter to exit the program. . . ')

def friends_define(key,p_steamid):
    list_url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v1/?key='+key+'&steamid='+p_steamid
    list_r = requests.get(list_url).json()
    list = list_r['friendslist']['friends']

    steamids_list = []
    for item in list:
        steamids_list.append(item['steamid'])
    steamids = ','.join(steamids_list)
    print(steamids)

    user_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+key+'&steamids='+steamids
    user_r = requests.get(user_url).json()
    print(user_r)
    
#heropool(key)
#API_recall(key,account_id)
#API_recall_2(key,account_id)
friends_define(key,p_steamid)
