import socket
import asyncio
import sys
import time
import threading

host = "127.0.0.1"
port = 10021

disconnectFlag = False
receive_message = "None"
send_message = ""
    
    
def updateMessage_receive():
    global receive_message, disconnectFlag
    print("init!")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        while disconnectFlag == False:
            data = b"None"
            data = client.recv(1024)
            if data != b"None":
                data = data.decode('utf-8')
                if data[5] != 'U':continue
                receive_message = data
                print("Client", receive_message)
                if receive_message[13] == '1':break


def sendMessage(message):   #サーバーに送るメッセージの保存
    global send_message
    send_message = "[FromPython]: "+message+'\n'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        client.send(send_message.encode('utf-8'))
        send_message = ""
    
def okMessage():
    global send_message
    if send_message == "":return True
    return False
    
def receiveMessage():       #受け取って保存してたメッセージを返す
    return receive_message

def resetMessage():         #保存してるメッセージの破棄
    global receive_message
    receive_message = "None"
    
def disconnectMessage():    #サーバーとの通信切断
    global disconnectFlag
    disconnectFlag = True

def initMessage():          #サーバーとの通信開始
    thread1 = threading.Thread(target=updateMessage_receive)
    thread1.start()






