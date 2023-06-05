import time
import random
import numpy as np
import copy
import heapq
from Board import *
from PlayerFunc import *

def get_hash(board, cnt = None):
    hash = ""
    for i in range(12*12):
        y, x = i//12, i%12
        idx = y*board.W+x
        char = ""
        if y >= board.H or x >= board.W:char = '0'
        elif idx == board.pos[0] or idx == board.pos[1]:char = '1'
        elif idx == board.pos[2] or idx == board.pos[3]:char = '2'
        elif board.color[idx] == COLOR_R:char = '3'
        elif board.color[idx] == COLOR_B:char = '4'
        else:char = '0'
        hash += char
    if cnt is not None:hash += str(cnt)
    return hash

class PlayerBeamSearch:
    def __init__(self, board, Color, cnt):
        self.board = board
        self.cnt = cnt
        self.old = cnt
        self.Color = Color      #0 : 1
        self.color = color1[Color]    #COLOR_R : COLOR_B
        self.best = rand_acts()
        self.best_cnt = 10
        
    
    def beam_search_single(self, player, width = 5, depth = 5, max_time = 2):   #1人分の動きをビームサーチ
        self.width = width
        self.depth = depth+1
        self.dic = []
        self.heap = []
        for i in range(self.depth):self.dic.append({})
        for i in range(self.depth):self.heap.append([])
        heapq.heappush(self.heap[0], (0, self.board, []))
        
        start = time.time()
        cnt = 0
        best = []   #best[最善手[score, [経路]], [[score, [経路]]...]
        for i in range(self.best_cnt):best.append((-INF, []))
        #時間いっぱいビームサーチを走らせる
        while(time.time()-start < max_time or cnt <= 300):
            if self.cnt != self.old or self.search == False:return 0
            cnt += 1
            for d in range(self.depth):
                if len(self.heap[d]) == 0:continue
                q = heapq.heappop(self.heap[d])
                #最大の深さまでたどったら
                if d == self.depth-1:
                    board = q[1]
                    score = board.calc_score()
                    if player < 2:score = score[0]-score[1]
                    if player >= 2:score = score[1]-score[0]
                    if best[-1][0] < score:
                        best[-1] = (score, q[2])
                        for i in range(self.best_cnt-1):
                            j = self.best_cnt-i-1
                            if best[j-1][0] >= score:break
                            best[j-1], best[j] = best[j], best[j-1]
                    continue
                #幅widthで探索
                s, v = move_sort_single(q[1], player)
                for i in range(self.width):
                    board = copy.deepcopy(q[1])
                    act = s[i]
                    score = v[i]-q[0]
                    acts = [[4, 0], [4, 0], [4, 0], [4, 0]]
                    acts[player][0] = act
                    board.move(acts)
                    hash = get_hash(board)
                    hand = copy.deepcopy(q[2])
                    hand.append(act)
                    if (hash in self.dic[d+1]) == False:
                        heapq.heappush(self.heap[d+1], (-score, board, hand))
                    self.dic[d+1][hash] = 1
        print("Beam Search Single Count:", cnt)
        for i in range(self.best_cnt):best[i] = best[i][1]      #[[経路1], [経路2]...]
        return best
        
        
    def beam_search_pair(self, color, width = 5*5, depth = 2, max_time = 2):    #1チーム分の動きをビームサーチ
        self.width = width
        self.depth = depth+1
        self.dic = []
        self.heap = []
        for i in range(self.depth):self.dic.append({})
        for i in range(self.depth):self.heap.append([])
        heapq.heappush(self.heap[0], (0, self.board, []))
        
        start = time.time()
        cnt = 0
        best = []
        for i in range(self.best_cnt):best.append((-INF, []))
        #時間いっぱいビームサーチを走らせる
        while(time.time()-start < max_time or best[-1][0] == -INF or cnt <= 30):
            if self.cnt != self.old or self.search == False:return 0
            cnt += 1
            for d in range(self.depth):
                if len(self.heap[d]) == 0:continue
                q = heapq.heappop(self.heap[d])
                #最大の深さまでたどったら
                if d == self.depth-1:
                    board = q[1]
                    score = board.calc_score()
                    if color == COLOR_R:score = score[0]-score[1]
                    if color == COLOR_B:score = score[1]-score[0]
                    if best[-1][0] < score:
                        best[-1] = (score, q[2])
                        for i in range(self.best_cnt-1):
                            j = self.best_cnt-i-1
                            if best[j-1][0] >= score:break
                            best[j-1], best[j] = best[j], best[j-1]
                        act = best[0][1][0]     #最善手の経路の初手
                        self.best = [[act//9, 0], [act%9, 0]]
                    continue
                #幅widthで探索
                #s = np.argsort(move_sort_pair(q[1], color))[::-1]
                s, v = move_sort_pair(q[1], color)
                for i in range(self.width):
                    board = copy.deepcopy(q[1])
                    act = s[i]
                    #score = board.predict_score(act, color)
                    #score += -q[0]
                    score = v[i]-q[0]
                    if color == COLOR_R:board.move([[act//9, 0], [act%9, 0], [4, 0], [4, 0]])
                    if color == COLOR_B:board.move([[4, 0], [4, 0], [act//9, 0], [act%9, 0]])
                    hash = get_hash(board)
                    hand = copy.deepcopy(q[2])
                    hand.append(act)
                    if (hash in self.dic[d+1]) == False:
                        heapq.heappush(self.heap[d+1], (-score, board, hand))
                    self.dic[d+1][hash] = 1
        print("Beam Search Count:", cnt)
        for i in range(self.best_cnt):best[i] = best[i][1]      ##[[経路1], [経路]2...]
        return best
        
    def search(self):
        print("Beam Search")
        self.best = rand_acts()
        self.search = True
        self.old = -1
        while self.search == True:
            if self.cnt != self.old:
                self.old = self.cnt
                s_time = time.time()
                #color, width = 5*5, depth = 2, max_time = 2
                self.beam_search_pair(color = self.color, width = 3*3, depth = 4, max_time = 2)
                print("Beam Search Done: {0}".format(time.time()-s_time))
        
    def stop_search(self):
        self.search = False
        
    def get_act(self):
        return self.best
        
        
        
if __name__ == '__main__':
    board = Board()
    player = PlayerBeamSearch(board, 0, 0)
    for i in range(1):
        act1 = player.beam_search_single(0)
        act2 = player.beam_search_single(1)
        print(act1)
        print(act2)
        act1 = act1[0][0]
        act2 = act2[0][0]
        act = create_acts([[act1, 0], [act2, 0]], rand_acts(), COLOR_R)
        print(act)
        board.move(act)
        board.print_board()
        print(board.calc_score())

        