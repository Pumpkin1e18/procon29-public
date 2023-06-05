import random
import numpy as np
import time
from BoardCreator import get_board

H, W = 8, 11

EMPTY = 0
PLAYER_R = 1
PLAYER_B = -1
COLOR_R = 2
COLOR_B = -2
DRAW = 3
INF = 1000000000

color1 = [COLOR_R, COLOR_B]
color2 = {COLOR_R:0, COLOR_B:1}
dv4 = [-W, -1, 1, W]
dv9 = [-W-1, -W, -W+1, -1, 0, 1, W-1, W, W+1]
MARKS={PLAYER_R:"●",PLAYER_B:"〇",EMPTY:"　",COLOR_R:"■",COLOR_B:"□",DRAW:"引き分け"}

class UnionFind:
    def __init__(self, n):
        self.ran = [0]*n
        self.par = [i for i in range(n)]
        
    def find(self, x):
        if self.par[x] == x:return x
        self.par[x] = self.find(self.par[x])
        return self.par[x]
        
    def unite(self, x, y):
        x = self.find(self.par[x])
        y = self.find(self.par[y])
        if x == y:return 0
        if self.ran[x] < self.ran[y]:self.par[x] = y
        else:
            self.par[y] = x
            if self.par[x] == self.par[y]:self.ran[x] += 1
            
    def same(self, x, y):
        return self.find(self.par[x]) == self.find(self.par[y])
        
        
class Board:
    def __init__(self, ty = 0, flag = True):    #ty: 種類(type), flag: True=赤: False=青
        global H, W, dv4, dv9
        H, W, self.number, self.pos = get_board(ty, flag)
        self.number = [flatten for inner in self.number for flatten in inner]
        self.color = [0]*H*W
        self.past_color = []
        self.past_pos = []
        for i in range(2):self.color[self.pos[i]] = COLOR_R
        for i in range(2):self.color[self.pos[i+2]] = COLOR_B
        dv4 = [-W, -1, 1, W]
        dv9 = [-W-1, -W, -W+1, -1, 0, 1, W-1, W, W+1]
        self.dv4, self.dv9 = dv4, dv9
        self.H, self.W = H, W
    def __lt__(self, other):
         return self.pos[0] < other.pos[0]
    
    def print_board(self):
        for i in range(H):
            for j in range(W):
                print("{0:3d}|".format(self.number[i*W+j]), end = '')
                if i*W+j == self.pos[0] or i*W+j == self.pos[1]:print(MARKS[PLAYER_R], end = '')
                elif i*W+j == self.pos[2] or i*W+j == self.pos[3]:print(MARKS[PLAYER_B], end = '')
                else:print(MARKS[self.color[i*W+j]], end = '')
            print("")
            for j in range(W):print("------", end = '')
            print("")
        for i in range(4):
            print("player{0}: ({1}, {2})".format(i+1, (self.pos[i]//W)+1, (self.pos[i]%W)+1))
    
    def ok(self, now, nxt):
        if nxt < 0 or H*W <= nxt:return False       #範囲外アクセス防止
        if abs(nxt%W - now%W) > 1:return False      #ワープ防止
        return True
        
    def check(self, v1, v2, pos, color):
        for i in range(2):
            v = v1 if i == 0 else v2
            if self.ok(pos[i], pos[i]+dv9[v]) == False:return False
            if self.color[pos[i]+dv9[v]] == color:return False
            
    def distance(self, player1, player2):   #プレイヤー間のマンハッタン距離を返す
        y1, x1 = self.pos[player1]//W, self.pos[player1]%W
        y2, x2 = self.pos[player2]//W, self.pos[player2]%W
        return abs(y1-y2)+abs(x1-x2)
        
    def predict_score(self, act, color):    #移動したときのスコアを大まかに見積もる
        pos = [self.pos[0], self.pos[1]]
        if color == COLOR_B:pos = [self.pos[2], self.pos[3]]
        score = 0
        for i in range(2):
            v = act//9 if i == 0 else act%9
            now, nxt = pos[i], pos[i]+dv9[v]
            if self.ok(now, nxt) == False or self.color[nxt] == color:continue
            if color == COLOR_R and (nxt == self.pos[2] or nxt == self.pos[3]):continue
            if color == COLOR_B and (nxt == self.pos[0] or nxt == self.pos[1]):continue
            score += self.number[nxt]
        return score
        
    def calc_value1(self, color):
        pos = None
        if color == COLOR_R:pos = [self.pos[0], self.pos[1]]
        else:pos = [self.pos[2], self.pos[3]]
        value, lst = [0]*18, [0]*9*9
        tmp = self.calc_score()
        origin = tmp[0]-tmp[1]
        for i in range(18):
            now, nxt = pos[i//9], pos[i//9]+dv9[i%9]
            if self.ok(now, nxt) == False or self.color[nxt] == color:continue
            if self.color[nxt] != EMPTY:value[i] = self.number[nxt]
            else:
                self.color[nxt] = color
                tmp = self.calc_score()
                value[i] = tmp[0]-tmp[1]-origin
                if color == COLOR_B:value[i] = -value[i]
                self.color[nxt] = EMPTY
        for i in range(9*9):
            if pos[0]+dv9[i//9] == pos[1]+dv9[i%9]:continue
            lst[i] = value[i//9]+value[(i%9)+9]
        return lst
        
    def dfs(self, now, c):
        if self.used[now] or self.color[now] == c:return 0
        self.used[now] = 1
        sum = 0
        flg = 0
        for i in range(4):
            nxt = now+dv4[i]
            if self.ok(now, nxt) == False:
                flg = 1
                continue
            tmp = self.dfs(nxt, c)
            if tmp == -1:flg = 1
            sum += tmp
        if flg:return -1
        return sum+abs(self.number[now])
        
    def calc_score(self):
        score_red = 0
        score_blue = 0
        self.used = [0]*H*W
        for i in range(H*W):
            score_red += max([self.dfs(i, COLOR_R), 0])
            if self.color[i] == COLOR_R:score_red += self.number[i]
        self.used = [0]*H*W
        for i in range(H*W):
            score_blue += max([self.dfs(i, COLOR_B), 0])
            if self.color[i] == COLOR_B:score_blue += self.number[i]
        return [score_red, score_blue]
        
    def move(self, vec):     #[[vector, bool]*4]
        MARKS = {0: COLOR_R, 1: COLOR_B}
        past_color = {}
        past_pos = [0]*4
        flg = [0]*4     #はがすかどうか
        nxt = [0]*4      #次の移動場所
        cnt = [0]*H*W       #その場所に行こうとしてる人数
        for i in range(4):
            nxt[i] = self.pos[i]+dv9[vec[i][0]]
            if self.ok(self.pos[i], nxt[i]) == False:nxt[i] = self.pos[i]
            if nxt[i] < 0 or H*W <= nxt[i]:nxt[i] = self.pos[i]
            if abs(nxt[i]%W - self.pos[i]%W) > 1:nxt[i] = self.pos[i]
            past_color[self.pos[i]] = MARKS[i//2]
            past_color[nxt[i]] = self.color[nxt[i]]
            past_pos[i] = self.pos[i]
            cnt[nxt[i]] += 1
            if self.color[nxt[i]] == -color1[i//2]:flg[i] = 1
            if self.color[nxt[i]] != EMPTY and vec[i][1]:flg[i] = 1
        self.past_color.append(past_color)
        self.past_pos.append(past_pos)
        
        for i in range(4):      #移動できない人たちの処理
            if cnt[nxt[i]] <= 1 and flg[i]:self.color[nxt[i]] = EMPTY
            if cnt[nxt[i]] > 1 or flg[i]:nxt[i] = self.pos[i];
        
        for i in range(4):
            self.pos[i] = nxt[i]
            self.color[nxt[i]] = color1[i//2]
        return [self.pos[i] for i in range(4)]
        
    def prev(self):
        past_color = self.past_color.pop()
        past_pos = self.past_pos.pop()
        for i in past_color:self.color[i] = past_color[i]
        for i in range(4):self.pos[i] = past_pos[i]
        
    def get_init_str(self):
        s = "0 "+str(H)+" "+str(W)+" "
        for i in range(H*W):s += str(self.number[i]) + " "
        for i in range(4):s += str(self.pos[i]//W)+" "+str(self.pos[i]%W)+" "
        return s
        
    def get_state_str(self):
        s = "1 "
        score = self.calc_score()
        color2 = {EMPTY: 0, COLOR_R: 1, COLOR_B: 2}
        for i in range(H*W):s += str(color2[self.color[i]]) + " "
        for i in range(4):s += str(self.pos[i]//W)+" "+str(self.pos[i]%W)+" "
        s += str(score[0])+" "+str(score[1])+" "
        return s


#board = Board()
#board.print_board()
