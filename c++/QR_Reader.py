# -*- coding: utf-8 -*-
import numpy
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import cv2


def reader():
    # 引数でカメラを選べれる
    cap = cv2.VideoCapture(0)
    
    while True:
        # VideoCaptureから1フレーム読み込む
        ret, frame = cap.read()
        
        #画像を表示する
        cv2.imshow('Raw Frame', frame)
        
        #QRコードを読み取る
        data = decode(frame)
        if data != []:
            data = data[0][0].decode('utf-8', 'ignore')
            #print(data)
            cap.release()
            cv2.destroyAllWindows()
            return data+" "
            break
    
        # キー入力を1ms待って、k が27（ESC）だったらBreakする
        k = cv2.waitKey(1)
        if k == 27:
            break
    
    # キャプチャをリリースして、ウィンドウをすべて閉じる
    cap.release()
    cv2.destroyAllWindows()

data = ""
p = 0
def get_num():      #dataからの数字取得
    global data, p
    s = ""
    while True:
        if data[p] == ' ' or data[p] == ':':break
        s += data[p]
        p += 1
    p += 1
    return int(s)
    
def width(H, W, pos1, pos2):
    pos3 = [pos1[0], W-1-pos1[1]]
    pos4 = [pos2[0], W-1-pos2[1]]
    return pos3, pos4
    
def height(H, W, pos1, pos2):
    pos3 = [H-1-pos1[0], pos1[1]]
    pos4 = [H-1-pos2[0], pos2[1]]
    return pos3, pos4
    
    

def get_board3():       #QRコードを使ったボード情報の取得
    global data, p
    data = reader()
    H = get_num()
    W = get_num()
    board = [[0]*W for i in range(H)]   #数字取得
    for i in range(H):
        for j in range(W):
            board[i][j] = get_num()
    pos = [[0, 0] for i in range(4)]      #味方のプレイヤー座標取得
    for i in range(2):
        for j in range(2):pos[i][j] = get_num()-1
    #相手のプレイヤー座標推定
    p_pos = [[[0, 0], [0, 0]], [[0, 0], [0, 0]]]
    
    """------------------------------------------------------------"""
    flag = True
    for i in range(H):          #x軸対象
        if board[i][0] != board[H-1-i][0]:flag = False
    if flag == True:pos[2], pos[3] = height(H, W, pos[0], pos[1])
    """------------------------------------------------------------"""
    
    """------------------------------------------------------------"""
    flag = True
    for i in range(W):          #y軸対象
        if board[0][i] != board[0][W-1-i]:flag = False
    if flag == True:pos[2], pos[3] = width(H, W, pos[0], pos[1])
    """------------------------------------------------------------"""
    
    p_pos[0][0], p_pos[0][1] = height(H, W, pos[0], pos[1])     #追加(x軸)
    p_pos[1][0], p_pos[1][1] = width(H, W, pos[0], pos[1])      #追加(y軸)
    for i in range(4):pos[i] = pos[i][0]*W+pos[i][1]    #座標圧縮
    
    #表示
    print(data, end = '')
    print("[{} {}:".format(pos[2]//W+1, pos[2]%W+1), end = '')
    print("{} {}]".format(pos[3]//W+1, pos[3]%W+1))
    #追加
    print("[{} {}:{} {}]".format(p_pos[0][0][0]+1, p_pos[0][0][1]+1, p_pos[0][1][0]+1, p_pos[0][1][1]+1), end='')
    print(" [{} {}:{} {}]".format(p_pos[1][0][0]+1, p_pos[1][0][1]+1, p_pos[1][1][0]+1, p_pos[1][1][1]+1))
    
    
    
if __name__ == '__main__':
    get_board3()
    




