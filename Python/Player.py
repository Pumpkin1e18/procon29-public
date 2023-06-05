import time
import random
import numpy as np
import copy
from Board import *
from PlayerFunc import *

#rand(s, t)     [s, t]の乱数
#rand_act()     1人分のランダムな動き
#rand_acts()    2人分のランダムな動き
#check(board, v1, v2, color)    無駄な動きの場合False
#move_sort(board, color)    次の動きの価値を保存したlistを返す


class PlayerHuman:
    def __init__(self):
        self.cnt = 0
        self.best = None
        
    def search(self):
        pass
        
    def stop_search(self):
        pass
        
    def get_act(self):
        return [[-1, -1], [-1, -1]]
        
        
class PlayerGreedy:
    def __init__(self, Board, Color, cnt):
        self.board = Board
        self.Color = Color      #0 : 1
        self.color = color1[Color]      #COLOR_R : COLOR_B
        self.cnt = cnt
        self.best = rand_acts()
        
    def greedy(self):
        s = np.argsort(move_sort(self.board, self.color))[::-1]
        self.best = [[s[0]//9, 0], [s[0]%9, 0]]
        return self.best
        
    def search(self):
        pass
        
    def stop_search(self):
        self.search = False
    
    def get_act(self):
        return self.greedy()


#s_time = time.time()
#if self.Flg:print("time: {0}".format(time.time()-s_time))
class PlayerAlphaBeta:
    def __init__(self, board, Color, cnt):
        self.board = board
        self.cnt = cnt
        self.old = cnt
        self.Color = Color      #0 : 1
        self.color = color1[Color]    #COLOR_R : COLOR_B
        self.best = rand_acts()
        
    def alphabeta(self, b, alpha, beta, color, width, cnt, max_cnt, hand):
        self.called += 1
        if cnt == max_cnt:
            score = b.calc_score()  #O(10^3)
            if self.color == COLOR_R:return score[0]-score[1]
            else:return score[1]-score[0]
            
        if color == self.color:
            s = np.argsort(move_sort(b, color))[::-1]
            if cnt == 0:s = np.argsort(b.calc_value1(color))[::-1]
            if self.cnt != self.old or self.search == False:return 0
            for i in range(width):
                hand = [[s[i]//9, 0], [s[i]%9, 0]]
                #if check(b, s[i]//9, s[i]%9, color) == False:continue   #注意
                res = self.alphabeta(b, alpha, beta, -color, width, cnt, max_cnt, hand)
                if cnt == 0 and res > alpha:self.best = hand
                alpha = max(alpha, res)
                if alpha >= beta:return alpha
            return alpha
        else:
            s = np.argsort(move_sort(b, color))[::-1]
            board = b
            board = copy.deepcopy(b)    #O(10^3)
            for i in range(width):
                if self.cnt != self.old or self.search == False:return 0
                #if check(b, s[i]//9, s[i]%9, color) == False:continue   #注意
                hand2 = copy.deepcopy(hand)
                hand2.extend([[s[i]//9, 0], [s[i]%9, 0]])
                if self.color == COLOR_B:
                    hand2[0], hand2[2] = hand2[2], hand2[0]
                    hand2[1], hand2[3] = hand2[3], hand2[1]
                board.move(hand2)
                res = self.alphabeta(board, alpha, beta, -color, width, cnt+1, max_cnt, None)
                board.prev()
                beta = min(beta, res)
                if alpha >= beta:return beta
            return beta
        
    def MTD(self, max_cnt):
        #board, alpha, beta, color, width, cnt, max_cnt, hand
        self.called = 0
        board = copy.deepcopy(self.board)
        res1 = self.alphabeta(board, -INF, INF, self.color, 2*2, 0, max_cnt, None)
        print("Alpha Beta predict {0}, called {1}".format(res1, self.called))
        self.called = 0
        res2 = self.alphabeta(board, res1+0, res1+1, self.color, 3*3, 0, max_cnt, None)
        res = res1
        if res2 == res+2:res = res2
        print("Alpha Beta predict {0}, called {1}".format(res, self.called))
        
    def search(self):
        print("Alpha Beta")
        self.best = rand_acts()
        self.search = True
        self.old = -1
        while self.search == True:
            if self.cnt != self.old:
                self.old = self.cnt
                s_time = time.time()
                self.MTD(3)
                #res = self.alphabeta(self.board, -INF, INF, self.color, 2, 0, 3, None)
                print("Alpha Beta Done: {0}".format(time.time()-s_time))
                #print("Alpha Beta predict {0}".format(res))
        
    def stop_search(self):
        self.search = False
        
    def get_act(self):
        return self.best

#player = PlayerRandom()
#print(player.get_act())



