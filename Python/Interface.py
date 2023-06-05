import time
import random
import copy
import sys
from Client import *
from Board import *
from Player import *
from PlayerBeamSearch import *
from PlayerAlphaSearch import *

H = 8
W = 11

#0: Human, 1: Greedy, 2: Alpha Beta 3: MCTS
player_red = 0
player_blue = 0
max_cnt = 120
cnt = 0

#[FromPython]: 0 h w number[h*w] pos[4]         初期化
#[FromPython]: 1 color[h*w] pos[4] score[2]         ゲーム進行
#[FromPython]: 2 [[v1[i], b1[i]], ...]      最善手(only first)予測

#[FromUnity]: 0 vector[i] bool[i]       移動
#[FromUnity]: 1         終了
#[FromUnity]: 2 color player    プレイヤーの選択
#[FromUnity]: 3         前のターンに戻る

#ty: 0:デフォルト, 1:なにもかもランダム(適当), 2:対称ランダム, 3:QRコード
board = Board(3, False)      #ty: 種類(type), flag: True=赤: False=青
def select_player(color, n, c):
    if n == 0:return PlayerHuman()
    if n == 1:return PlayerGreedy(board, color, c)
    if n == 2:return PlayerAlphaBeta(board, color, c)
    if n == 3:return PlayerBeamSearch(board, color, c)
    if n == 4:return PlayerAlphaSearch(board, color, c)

def get_vector_list(message):
    p = 15
    vec = [[0, 0] for i in range(4)]
    for i in range(4):
        vec[i][0] = int(message[p])
        vec[i][1] = int(message[p+2])
        p += 4
    return vec

def vector_to_str(vec):
    s = "2 "
    for i in range(4):
        s += str(vec[i][0]) + " "
        s += str(vec[i][1]) + " "
    return s
    
tmp1 = select_player(0, 0, 0)  #player_red      0 player 0
tmp2 = select_player(1, 0, 0)  #player_blue     1 player 0
player = [tmp1, tmp2]

thread = [None, None]
thread[0] = threading.Thread(target=player[0].search)
thread[1] = threading.Thread(target=player[1].search)
thread[0].start()
thread[1].start()

#---------------------------------------------------------
"""tmp1 = select_player(0, 4, 0)  #player_red  player  0
tmp2 = select_player(1, 1, 0)  #player_blue  player  0
player = [tmp1, tmp2]
thread = [None, None]
thread[0] = threading.Thread(target=player[0].search)
thread[1] = threading.Thread(target=player[1].search)
thread[0].start()
thread[1].start()
for i in range(1):
    for s in range(2):player[s].cnt = i
    time.sleep(5)
    act1 = player[0].get_act()
    act2 = player[1].get_act()
    act = copy.deepcopy(act1)
    act.extend(act2)
    board.move(act)
    board.print_board()
    print(act)
    print(board.calc_score())
    print("")
for i in range(2):player[i].stop_search()
print(board.calc_score())"""
#---------------------------------------------------------
initMessage()
sendMessage(board.get_init_str())
time.sleep(1)
sendMessage(board.get_state_str())
s_time = time.time()
while 1:
    time.sleep(0.1)
    for i in range(2):player[i].cnt = cnt
    if time.time()-s_time > 1:
        if okMessage() == False:continue
        act1 = player[0].get_act()
        act2 = player[1].get_act()
        act = copy.deepcopy(act1)
        act.extend(act2)
        sendMessage(vector_to_str(act))
        s_time = time.time()
        #print(act)
        continue
    message = receiveMessage()
    if message == "None":continue
    if message[5] != 'U':continue
    print(message)
    
    if message[13] == '0':
        board.move(get_vector_list(message))
        sendMessage(board.get_state_str())
        resetMessage()
        print(get_vector_list(message))
        board.print_board()
        cnt += 1
    elif message[13] == '1':break
    elif message[13] == '2':
        print("select player: {0} {1}".format(message[15], message[17]))
        color = int(message[15])
        player_num = int(message[17])
        player[color].stop_search()
        player[color] = select_player(color, player_num, cnt)
        thread[color] = threading.Thread(target=player[color].search)
        thread[color].start()
        resetMessage()
    elif message[13] == '3':
        print("prev")
        resetMessage()
        board.prev()
        board.print_board()
        sendMessage(board.get_state_str())
        cnt -= 1
    
    print("count", cnt+1)
    if cnt == max_cnt:break
for i in range(2):player[i].stop_search()
time.sleep(1)
disconnectMessage()



