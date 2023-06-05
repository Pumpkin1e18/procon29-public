import time
import random
import numpy as np
import copy
import heapq
from Board import *
from PlayerFunc import *
from PlayerBeamSearch import *

class PlayerAlphaSearch:
    def __init__(self, board, Color, cnt):
        self.board = board
        self.cnt = cnt
        self.old = cnt
        self.Color = Color      #0 : 1
        self.color = color1[Color]    #COLOR_R : COLOR_B
        self.best_cnt = 5
        self.single_depth = 5
        self.pair_depth = 5
        self.depth = min(self.single_depth, self.pair_depth)
        self.player = PlayerBeamSearch(board, Color, cnt)
        self.player.best_cnt = self.best_cnt
        self.best = rand_acts()
        
    
    #ビームサーチした結果を保存する
    def make_history(self):
        self.his = []
        for i in range(4):
            tmp = []
            for j in range(self.depth):tmp.append({})
            self.his.append(tmp)
        act = None
        #print(np.array(self.acts).shape)
        #for i in range(4):print(self.acts[i])
        for i in range(4):
            for j in range(self.best_cnt):
                s = ""
                for k in range(self.depth):
                    if self.acts[i] is None:act = self.acts[i-1][j][k]%9
                    elif i+1 < 4 and self.acts[i+1] is None:act = self.acts[i][j][k]//9
                    else:act = self.acts[i][j][k]
                    if (s in self.his[i][k]) == False:self.his[i][k][s] = [act]
                    else:self.his[i][k][s].append(act)
                    s += str(act)
        
    def make_history_alpha(self, acts):
        if acts is None:return 0
        size = len(acts)
        for i in range(4):
            s = ""
            for j in range(size//4):
                act = int(acts[4*j+i])
                if (s in self.hash[i]) == False:self.hash[i][s] = [act]
                else:self.hash[i][s].append(act)
                s += acts[4*j+i]
        #print("")
        #print(self.hash)
        #print("")
        
    #αβ探索
    def alphabeta(self, b, alpha, beta, color, cnt, max_cnt, state, hand, s1="", s2="", s3="", s4=""):
        if self.cnt != self.old or self.search == False:return 0, ""
        self.called += 1
        #葉まで到達したときスコアを返す
        if cnt == max_cnt:
            score = b.calc_score()
            if self.color == COLOR_R:return score[0]-score[1], ""
            else:return score[1]-score[0], ""
            
        idx = [0, 1]
        if color == COLOR_B:idx = [2, 3]
        width = state//100
        way = None
        search_f = True
        #自分の色なら
        if color == self.color:
            handed = {}
            s = np.argsort(move_sort(b, color))[::-1]
            #if cnt == 0:s = np.argsort(b.calc_value1(color))[::-1]
            #過去のAlphaBetaの結果をもとに行動
            if (s1 in self.hash[idx[0]]) and (s2 in self.hash[idx[1]]):
                acts1 = self.hash[idx[0]][s1]
                acts2 = self.hash[idx[1]][s2]
                for i in range(len(acts1)):
                    for j in range(len(acts2)):
                        if acts1[i]*9+acts2[j] in handed or search_f == False:continue
                        #if cnt == 0:print(state)
                        if (state%100)//10 == 0:continue
                        handed[acts1[i]*9+acts2[j]] = 1
                        hand = [[acts1[i], 0], [acts2[j], 0]]
                        ss1, ss2 = s1+str(acts1[i]), s2+str(acts2[j])
                        res, ways = self.alphabeta(b, alpha, beta, -color, cnt, max_cnt, state, hand, ss1, ss2, s3, s4)
                        if cnt == 0 and res > alpha:
                            self.best = hand
                            print("alpha", hand)
                        if res > alpha and ways is not None:
                            way = str(acts1[i])+str(acts2[j])+ways
                            #if cnt == 0:print(way)
                        alpha = max(alpha, res)
                        if alpha >= beta:search_f = False
            #貪欲に上から数手探索
            #if cnt == 0:print(state)
            for i in range(width):
                if s[i] in handed or search_f == False:continue
                #if cnt == 0:print("*alpha beta*", s[i]//9, s[i]%9)
                handed[s[i]] = 1
                hand = [[s[i]//9, 0], [s[i]%9, 0]]
                ss1, ss2 = s1+str(s[i]//9), s2+str(s[i]%9)
                res, ways = self.alphabeta(b, alpha, beta, -color, cnt, max_cnt, state, hand, ss1, ss2, s3, s4)
                if cnt == 0 and res > alpha:
                    print("greedy", hand)
                    self.best = hand
                if res > alpha and ways is not None:
                    way = str(s[i]//9)+str(s[i]%9)+ways
                    #if cnt == 0:print(way)
                alpha = max(alpha, res)
                if alpha >= beta:search_f = False
            #return alpha
            #if state == 0:search_f = False
            #ビームサーチの結果をもとに行動
            if (s1 in self.his[idx[0]][cnt]) and (s2 in self.his[idx[1]][cnt]):
                #print("called")
                acts1 = self.his[idx[0]][cnt][s1]
                acts2 = self.his[idx[1]][cnt][s2]
                for i in range(len(acts1)):
                    for j in range(len(acts2)):
                        if acts1[i]*9+acts2[j] in handed or search_f == False:continue
                        if state%10 == 0:continue
                        handed[acts1[i]*9+acts2[j]] = 1
                        hand = [[acts1[i], 0], [acts2[j], 0]]
                        ss1, ss2 = s1+str(acts1[i]), s2+str(acts2[j])
                        res, ways = self.alphabeta(b, alpha, beta, -color, cnt, max_cnt, state, hand, ss1, ss2, s3, s4)
                        if cnt == 0 and res > alpha:
                            print("beam search", hand)
                            self.best = hand
                        if res > alpha and ways is not None:
                            way = str(acts1[i])+str(acts2[j])+ways
                            ##if cnt == 0:print(way)
                        alpha = max(alpha, res)
                        if alpha >= beta:search_f = False
            return alpha, way
        else:   #相手の行動
            handed = {}
            s = np.argsort(move_sort(b, color))[::-1]
            board = b
            #board = copy.deepcopy(b)
            #過去のAlphaBetaの結果をもとに行動
            if (s3 in self.hash[idx[0]]) and (s4 in self.hash[idx[1]]):
                acts1 = self.hash[idx[0]][s3]
                acts2 = self.hash[idx[1]][s4]
                for i in range(len(acts1)):
                    for j in range(len(acts2)):
                        if acts1[i]*9+acts2[j] in handed or search_f == False:continue
                        if (state%100)//10 == 0:continue
                        handed[acts1[i]*9+acts2[j]] = 1
                        hand2 = copy.deepcopy(hand)
                        hand2.extend([[acts1[i], 0], [acts2[j], 0]])
                        if self.color == COLOR_B:
                            hand2[0], hand2[2] = hand2[2], hand2[0]
                            hand2[1], hand2[3] = hand2[3], hand2[1]
                        ss1, ss2 = s3+str(acts1[i]), s4+str(acts2[j])
                        board.move(hand2)
                        res, ways = self.alphabeta(board, alpha, beta, -color, cnt+1, max_cnt, state, None, s1, s2, ss1, ss2)
                        board.prev()
                        if res < beta and ways is not None:way = str(acts1[i])+str(acts2[j])+ways
                        beta = min(beta, res)
                        if alpha >= beta:search_f = False
            #貪欲に上から数手探索
            for i in range(width):
                if s[i] in handed or search_f == False:continue
                handed[s[i]] = 1
                hand2 = copy.deepcopy(hand)
                hand2.extend([[s[i]//9, 0], [s[i]%9, 0]])
                if self.color == COLOR_B:
                    hand2[0], hand2[2] = hand2[2], hand2[0]
                    hand2[1], hand2[3] = hand2[3], hand2[1]
                ss1, ss2 = s3+str(s[i]//9), s4+str(s[i]%9)
                board.move(hand2)
                res, ways = self.alphabeta(board, alpha, beta, -color, cnt+1, max_cnt, state, None, s1, s2, ss1, ss2)
                board.prev()
                if res < beta and ways is not None:way = str(s[i]//9)+str(s[i]%9)+ways
                beta = min(beta, res)
                if alpha >= beta:search_f = False
            #return beta
            #if state == 0:search_f = False
            #ビームサーチの結果をもとに行動
            if (s3 in self.his[idx[0]][cnt]) and (s4 in self.his[idx[1]][cnt]):
                acts1 = self.his[idx[0]][cnt][s3]
                acts2 = self.his[idx[1]][cnt][s4]
                for i in range(len(acts1)):
                    for j in range(len(acts2)):
                        if acts1[i]*9+acts2[j] in handed or search_f == False:continue
                        if state%10 == 0:continue
                        handed[acts1[i]*9+acts2[j]] = 1
                        hand2 = copy.deepcopy(hand)
                        hand2.extend([[acts1[i], 0], [acts2[j], 0]])
                        if self.color == COLOR_B:
                            hand2[0], hand2[2] = hand2[2], hand2[0]
                            hand2[1], hand2[3] = hand2[3], hand2[1]
                        ss1, ss2 = s3+str(acts1[i]), s4+str(acts2[j])
                        board.move(hand2)
                        res, ways = self.alphabeta(board, alpha, beta, -color, cnt+1, max_cnt, state, None, s1, s2, ss1, ss2)
                        board.prev()
                        if res < beta and ways is not None:way = str(acts1[i])+str(acts2[j])+ways
                        beta = min(beta, res)
                        if alpha >= beta:search_f = False
            return beta, way
    
    def MTD(self):
        #board, alpha, beta, color, cnt, max_cnt, state, hand, s1="", s2="", s3="", s4=""
        start = time.time()
        self.hash = [{}, {}, {}, {}]
        board = copy.deepcopy(self.board)
        alpha, beta = -INF, INF
        for i in range(3):
            if self.cnt != self.old or self.search == False:return 0
            self.called = 0
            #state = width*100+alphabeta+beamsearch
            state = 100*(3-i)*2+1*10+1
            res, way = self.alphabeta(board, alpha, beta, self.color, 0, min(3+i, self.depth), state, None)
            self.make_history_alpha(way)
            print("Alpha Beta predict {0}, called {1}".format(res, self.called))
            alpha, beta = res-10, res+10
        print(time.time()-start, "s")
        """for i in range(3):
            if self.cnt != self.old or self.search == False:return 0
            self.called = 0
            #state = width*100+alphabeta+beamsearch
            state = 100*(i+1)+1*10+1
            if i == 0:state = 300
            res, way = self.alphabeta(board, alpha, beta, self.color, 0, self.depth, state, None)
            #print("way = ")
            #if way is not None:
            #    for i in range(4):
            #        for j in range(5):print(way[j*4+i], end = ' ')
            #        print("")
            #else:print("None")
            self.make_history_alpha(way)
            print("Alpha Beta predict {0}, called {1}".format(res, self.called))
            alpha, beta = res-6, res+6"""
            
        
    def alpha_search(self):
        self.acts = [None, None, None, None]    #player i, 上からj番目, k手目
        board = copy.deepcopy(self.board)
        #プレイヤー間の距離に応じてビームサーチ
        for i in range(2):
            if board.distance(2*i, 2*i+1) <= 4:
                print("pair")
                self.acts[2*i] = self.player.beam_search_pair(color1[i], width=2*2, depth=self.pair_depth, max_time=1)
            else:
                print("single")
                self.acts[2*i] = self.player.beam_search_single(2*i, width=3, depth=self.single_depth, max_time=0.5)
                self.acts[2*i+1] = self.player.beam_search_single(2*i+1, width=3, depth=self.single_depth, max_time=0.5)
        #ビームサーチの結果保存
        self.his = [{}, {}, {}, {}]
        self.make_history()
        #MTD
        self.MTD()
        return self.best
        
    def greedy(self):
        s = np.argsort(move_sort(self.board, self.color))[::-1]
        return [[s[0]//9, 0], [s[0]%9, 0]]
        
    def search(self):
        print("Alpha Search")
        self.best = rand_acts()
        self.search = True
        self.old = -1
        while self.search == True:
            if self.cnt != self.old:
                self.best = self.greedy()
                self.old = self.cnt
                s_time = time.time()
                #width = 5*5, depth = 2, max_time = 2
                self.alpha_search()
                print("Alpha Search Done: {0}".format(time.time()-s_time))
        
    def stop_search(self):
        self.search = False
        
    def get_act(self):
        return self.best
        



from Player import *
if __name__ == '__main__':
    board = Board(3)
    player1 = PlayerAlphaSearch(board, 0, 0)
    player2 = PlayerGreedy(board, 1, 0)
    for i in range(10):
        act1 = player1.alpha_search()
        act2 = player2.greedy()
        act = create_acts(act1, act2, COLOR_R)
        print(act)
        board.move(act)
        board.print_board()
        print(board.calc_score())
        print("")
        
        