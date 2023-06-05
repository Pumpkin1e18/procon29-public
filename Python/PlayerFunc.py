import time
import random
import copy
import numpy as np
from Board import *

def rand(s, t):
    return random.randint(s, t)

def rand_act():
    return [rand(0, 8), rand(0, 1)]
    
def rand_acts():
    return [rand_act(), rand_act()]
    
def create_acts(act1, act2, color):
    act = copy.deepcopy(act1)
    act.extend(act2)
    if color == COLOR_B:
        act[0], act[2] = act[2], act[0]
        act[1], act[3] = act[3], act[1]
    return act
    
def check(board, v1, v2, color):
    dv9 = board.dv9
    pos = None
    v = None
    if color == COLOR_R:pos = [board.pos[0], board.pos[1]]
    else:pos = [board.pos[2], board.pos[3]]
    for i in range(2):
        if i == 0:v = v1
        else:v = v2
        if board.ok(pos[i], pos[i]+dv9[v]) == False:return False
        if board.color[pos[i]+dv9[v]] == color:return False
    return True
    
def move_sort_single(board, player):
    dv9 = board.dv9
    lst = [0]*9
    pos = board.pos[player]
    for i in range(9):
        now, nxt = pos, pos+dv9[i]
        if board.ok(now, nxt) == False or now == nxt:
            lst[i] = -20
            continue
        if player < 2 and board.color[nxt] == COLOR_R:continue      #自分の色のマスはパス
        if player >= 2 and board.color[nxt] == COLOR_B:continue     #自分の色のマスはパス
        if player < 2 and (nxt == board.pos[2] or nxt == board.pos[3]):continue      #相手のいるマスはパス
        if player >= 2 and (nxt == board.pos[0] or nxt == board.pos[1]):continue     #相手のいるマスはパス
        lst[i] = board.number[nxt]
    arg = np.argsort(lst)[::-1]
    v = []
    for i in range(9):v.append(lst[arg[i]])
    return arg, v
    
def move_sort_pair(board, color):
    dv9 = board.dv9
    lst = [0]*9*9
    score = [0, 0]
    pos = None
    if color == COLOR_R:pos = [board.pos[0], board.pos[1]]
    else:pos = [board.pos[2], board.pos[3]]
    for i in range(9*9):
        now1, nxt1 = pos[0], pos[0]+dv9[i//9]
        now2, nxt2 = pos[1], pos[1]+dv9[i%9]
        if board.ok(now1, nxt1) == False or board.ok(now2, nxt2) == False:  #ボード外アクセス
            lst[i] = -40
            continue
        if nxt1 == nxt2:continue
        score[0] = board.number[nxt1]
        score[1] = board.number[nxt2]
        if board.color[nxt1] == color:score[0] = 0      #同じ色なら加点しない
        if board.color[nxt2] == color:score[1] = 0      #同じ色なら加点しない
        if now1 == nxt1:score[0] = -1       #とどまるのは減点
        if now2 == nxt2:score[1] = -1       #とどまるのは減点
        if color == COLOR_R:        #相手のいるマスは減点
            if nxt1 == board.pos[2] or nxt1 == board.pos[3]:score[0] = min(score[0], 0)
            if nxt2 == board.pos[2] or nxt2 == board.pos[3]:score[1] = min(score[1], 0)
        if color == COLOR_B:        #相手のいるマスは減点
            if nxt1 == board.pos[0] or nxt1 == board.pos[1]:score[0] = min(score[0], 0)
            if nxt2 == board.pos[0] or nxt2 == board.pos[1]:score[1] = min(score[1], 0)
        lst[i] = score[0]+score[1]
    arg = np.argsort(lst)[::-1]
    return arg, lst

def move_sort(board, color):
    dv9 = board.dv9
    lst = [0]*9*9
    score = [0, 0]
    pos = None
    if color == COLOR_R:pos = [board.pos[0], board.pos[1]]
    else:pos = [board.pos[2], board.pos[3]]
    for i in range(9*9):
        now1, nxt1 = pos[0], pos[0]+dv9[i//9]
        now2, nxt2 = pos[1], pos[1]+dv9[i%9]
        if board.ok(now1, nxt1) == False or board.ok(now2, nxt2) == False:  #ボード外アクセス
            lst[i] = -40
            continue
        if nxt1 == nxt2:continue
        score[0] = board.number[nxt1]
        score[1] = board.number[nxt2]
        if board.color[nxt1] == color:score[0] = 0      #同じ色なら加点しない
        if board.color[nxt2] == color:score[1] = 0      #同じ色なら加点しない
        if now1 == nxt1:score[0] = -1       #とどまるのは減点
        if now2 == nxt2:score[1] = -1       #とどまるのは減点
        lst[i] = score[0]+score[1]
    return lst
    
    
    