// server
#include <stdio.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <thread>
#include <vector>
using namespace std;

#define PORT 10021 //ポート番号

// g++ -o server server.cpp -lws2_32
// http://onishi-lab.jp/programming/tcp_win.html

int k = 0, n = 3;
vector<thread> threads(n);
vector<int> vec(n, -1);

// 全員に送る
void send_all(char buffer[1024], size_t len){
  for(int i = 0;i < n;i++){
    if(vec[i] == -1)continue;
    // send(dstSocket, buffer, sizeof(buffer), 0);
    send(vec[i], buffer, len, 0);
  }
}

// 自分以外に送る
void send_chat(char buffer[1024], size_t len, int id){
  for(int i = 0;i < n;i++){
    if(vec[i] == -1 or i == id)continue;
    send(vec[i], buffer, len, 0);
  }
}

// 接続者と通信
void communicate(int id, int dstSocket){
  if(id == -1)return;
  int status;
  vec[id] = dstSocket;
  while(1){
    char buffer[1024] = "";
    //パケットの受信
    int numrcv = recv(dstSocket, buffer, sizeof(buffer), 0);
    if(numrcv ==0 || numrcv ==-1 ){
      printf("接続が切れました\n\n");
      status = closesocket(dstSocket); break;
    }
    printf("%s\n", buffer);
    // パケットの送信
    send_chat(buffer, sizeof(buffer), id);
    // send(dstSocket, buffer, sizeof(buffer), 0);
  }
  vec[id] = -1;
}

// メイン関数
int main() {
  SetConsoleOutputCP( 65001 );
	int i;
	// ポート番号，ソケット
	int srcSocket;  // 自分
	int dstSocket;  // 相手
  
	// sockaddr_in 構造体
	struct sockaddr_in srcAddr;
	struct sockaddr_in dstAddr;
	int dstAddrSize = sizeof(dstAddr);
	int status;
	// 各種パラメータ
	int numrcv;
	char buffer[1024];
  
	// Windows の場合
	WSADATA data;
	WSAStartup(MAKEWORD(2,0), &data);
	// sockaddr_in 構造体のセット
	memset(&srcAddr, 0, sizeof(srcAddr));
	srcAddr.sin_port = htons(PORT);
	srcAddr.sin_family = AF_INET;
	srcAddr.sin_addr.s_addr = htonl(INADDR_ANY);

	// ソケットの生成（ストリーム型）
	srcSocket = socket(AF_INET, SOCK_STREAM, 0);
  	// ソケットのバインド
	bind(srcSocket, (struct sockaddr *) &srcAddr, sizeof(srcAddr));
  	// 接続の許可
	listen(srcSocket, 1);
  
  
  for(int i = 0;i < n;i++)threads[i] = thread(communicate, -1, -1);
 	while(1){ //ループで回すことによって何度でもクライアントからつなぐことができる
		// 接続の受付け
		printf("接続を待っています\nクライアントプログラムを動かしてください\n");
		dstSocket = accept(srcSocket, (struct sockaddr *) &dstAddr, &dstAddrSize);
		printf("%s から接続を受けました\n", inet_ntoa(dstAddr.sin_addr));
    
    while(vec[k] != -1)k = (k+1)%n;
    threads[k].join();
    threads[k] = thread(communicate, k, dstSocket);
	}
  for(int i = 0;i < n;i++)threads[i].join();
	// Windows での終了設定
	WSACleanup();

	return(0);
}