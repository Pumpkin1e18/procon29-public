import random
import numpy as np
import time
from QR_Reader import get_board3
#H W:number[0]:number[1]:~:number[H-1]:player1.y player1.x:player2.y player2.x:
"""
8 11:-2 1 0 1 2 0 2 1 0 1 -2:1 3 2 -2 0 1 0 -2 2 3 1:1 3 2 1 0 -2 0 1 2 3 1:2 1 1
2 2 3 2 2 1 1 2:2 1 1 2 2 3 2 2 1 1 2:1 3 2 1 0 -2 0 1 2 3 1:1 3 2 -2 0 1 0 -2 2 3
1:-2 1 0 1 2 0 2 1 0 1 -2:2 2:7 10:
"""

#盤面はマス80~144 約(9~12)
#各マスの点数-16~16
#最大ターン数は事前に分かる
#最大12試合,24チームが一度に行う
#負のポイントは20％程度(確か)

H = 8
W = 11
pos = [0]*4
board = [[-2, 1, 0, 1, 2, 0, 2, 1, 0, 1, -2],
        [1, 3, 2, -2, 0, 1, 0, -2, 2, 3, 1],
        [1, 3, 2, 1, 0, -2, 0, 1, 2, 3, 1],
        [2, 1, 1, 2, 2, 3, 2, 2, 1, 1, 2],
        [2, 1, 1, 2, 2, 3, 2, 2, 1, 1, 2],
        [1, 3, 2, 1, 0, -2, 0, 1, 2, 3, 1],
        [1, 3, 2, -2, 0, 1, 0, -2, 2, 3, 1],
        [-2, 1, 0, 1, 2, 0, 2, 1, 0, 1, -2]]
#for i in range(H):
#    for j in range(W):board[i][j] = abs(board[i][j])
playerPos = [[2-1, 10-1], [7-1, 2-1], [2-1, 2-1], [7-1, 10-1]]
for i in range(4):pos[i] = playerPos[i][0]*W+playerPos[i][1]

def get_HW():
    H = random.randint(7, 12)
    tmp = 0
    for i in range(20):
        if(i*H >= 80):
            tmp = i
            break
    W = random.randint(tmp, 12)
    return (H, W)
    
def get_num():
    tmp = random.randint(1, 10)
    score = random.randint(0, 16)
    if(tmp <= 2):score = -score
    return score
    
def get_board1():
    H, W = get_HW()
    board = [[0]*W for i in range(H)]
    for i in range(H*W):board[i//W][i%W] = get_num()
    lst = [i for i in range(H*W)]
    pos = np.random.choice(lst, 4, replace=False)
    return (H, W, board, pos)

def get_board2():
    H, W = get_HW()
    board = [[0]*W for i in range(H)]
    for i in range(H*W):board[i//W][i%W] = get_num()
    lst = []
    for i in range(H*W):
        y, x = i//W, i%W
        if H%2 == 1 and H//2 == y:continue
        if W%2 == 1 and W//2 == x:continue
        lst.append(i)
    pos = np.random.choice(lst, 4, replace=False)
    if random.randint(0, 1) == 0:   #y軸
        for i in range(2):
            y, x = pos[i]//W, pos[i]%W
            pos[i+2] = y*W+(W-x-1)
        for i in range(H*W):
            y, x = i//W, i%W
            if x < (W+1)//2:continue
            board[y][x] = board[y][W-x-1]
    else:   #x軸
        for i in range(2):
            y, x = pos[i]//W, pos[i]%W
            pos[i+2] = (H-y-1)*W+x
        for i in range(H*W):
            y, x = i//W, i%W
            if y < (H+1)//2:continue
            board[y][x] = board[H-y-1][x]
    return (H, W, board, pos)
    






def get_board(ty = 0, flag = True):
    global H, W, board, pos
    if(ty == 0):return (H, W, board, pos)
    if ty == 1:H, W, board, pos = get_board1()
    if ty == 2:H, W, board, pos = get_board2()
    if ty == 3:H, W, board, pos = get_board3()
    if flag == False:
        pos[0], pos[2] = pos[2], pos[0]
        pos[1], pos[3] = pos[3], pos[1]
    return (H, W, board, pos)


if __name__ == '__main__':
    H, W, board, pos, get_board(3)
    time.sleep(5)
    """print("H =", H)
    print("W =", W)
    for i in range(H):print(board[i])
    for i in range(4):print(pos[i]//W, pos[i]%W)"""




