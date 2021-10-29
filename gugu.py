from utils import load_jsonlines
import logging
import dota2api 
api = dota2api.Initialise('E2A0A78AB4A6C4BAEEA095E3F6F08154')
logger =logging.getLogger('__file__')
import time 
TIME_START = int(time.mktime(time.strptime('2021-10-25 00:00:00', '%Y-%m-%d %H:%M:%S')))

def check_winner(match_id, name_list):
    '''
    inp: match_id and name ids
    return :
        1 win
        0 lose
    '''
    winner_flag = -1
    hist = api.get_match_details(match_id=match_id)
    player_id = name_id_map[name_list[0]]
    if hist['radiant_win']:
        winner_flag=0
    else:
        winner_flag=1
    player=hist['players']
    player_win = None
    for i in player:
        if i['account_id'] == player_id:
            player_win = i['player_slot']//128
    if winner_flag == player_win:
        return 1
    else:
        return 0




def get_rank_match(id_num):
    match = []
    match_his = api.get_match_history(account_id=id_num)['matches']
    for i in match_his:
        if i['lobby_type']==7 and i['start_time']>TIME_START: #filter rank match 
            '''
            todo: add time split
            '''
            match.append(i)
    return match

def calc_match_rate(match_dict):
    match_play_tmp = {}
    for name, match in match_dict.items():
        for i in match:
            if i['match_id'] in match_play_tmp:
                match_play_tmp[i['match_id']].append(name)
            else:
                match_play_tmp[i['match_id']] = [name]
    match_play = {}       
    for k, v in match_play_tmp.items():
        if len(v)>=2:
            match_play[k]=v
    # print(match_play)   
    player_map ={}
    for name, _ in name_id_map.items():
        player_map[name] = {'win':0, 'lose':0}
    for k,v in match_play.items():
        win_flag = check_winner(k, v)
        if win_flag==1:
            win, lose = 1, 0
        else:
            win, lose = 0, 1
        for name in v:
            player_map[name]['win']+=win
            player_map[name]['lose']+=lose

    # print(player_map)
    return player_map

        
    

def gugugu():
    player = load_jsonlines('./player_en.json')
    print(player)
    global name_id_map
    name_id_map={}
    match_dict = {}
    for i in player:
        name_id_map[i['name']] = i['id']
        try:
            match_dict[i['name']] = get_rank_match(i['id'])
        except:
            logger.error('Can\'t  get {} : {} match history'.format(i['name'], i['id']) )
    player_map = calc_match_rate(match_dict)
    print(player_map)
    for name, win_lose in player_map.items():
        print("\nplayer : {}".format(name))
        
        print("game_sum : {}".format((win_lose['win']+win_lose['lose'])))
        print("win : {}".format(win_lose['win']))
        print("lose : {}".format(win_lose['lose']))
        win_rate = win_lose['win']/(win_lose['win']+win_lose['lose']+0.0)
        print("win_rate : {:.2f}%".format(win_rate*100))





if __name__ == "__main__":
    gugugu()