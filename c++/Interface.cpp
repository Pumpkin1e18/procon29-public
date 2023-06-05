#include "client.h"
#include "Board.h"
#include "CreateBoard.h"
#include "Player.h"
#include "header.h"


// 自分用実行メモ
// chcp 65001
// make

// [FromPython]: 0 h w number[h*w] pos[4]         初期化
// [FromPython]: 1 color[h*w] pos[4] score[2]         ゲーム進行
// [FromPython]: 2 [[v1[i], b1[i]], ...]      最善手(only first)予測
// 
// [FromUnity]: 0 vector[i] bool[i]       移動
// [FromUnity]: 1         終了
// [FromUnity]: 2 color player    プレイヤーの選択
// [FromUnity]: 3         前のターンに戻る
// [FromUnity]: 4 Y X

// 変数宣言
int h, w, pos[4];
vi number, color;
// 関数宣言
void game(int CG, int MA, int MT, int B, int DEG, int COL);
void game_CUI(int MT);
void game_GUI(int MA, int MT);
void select_disp(vi vec[2]);

// 試合情報
// 1回戦            :(H,W) = (11,8), max_turn = 40
// 2回戦            :(H,W) = (11,8), max_turn = 40
// 3回戦(準々決勝)   :(H,W) = (12,9), max_turn = 40
// 4回戦(準決勝)     :(H,W) = (12,10), max_turn = 40
// 5回戦(決勝)       :(H,W) = (12,12), max_turn = 40

// 確認事項
// max_turn
// 線対象
// 自分の色 typedef(2), degree, color



// 環境設定
/*--------------------------------------------------------------------------*/
// プレイヤー選択
// PlayerRandom, PlayerRnaom, PlayerHuman, PlayerAlphaBeta
typedef PlayerHuman PLAYER1;  // 赤チームのプレイヤー選択
typedef PlayerAlphaBeta PLAYER2;      // 青チームのプレイヤー選択

signed main(){
  SetConsoleOutputCP( 65001 );  // UTF-8にセットする
  int CG = GUI;     // CUI:コマンドプロンプト, GUI;Unity
  int MA = MANUAL;  // MANUAL:人が操作, AUTO:自動でゲーム進行
  int B = 2;        // ボード選択 0:デフォルト, 1:ランダム, 2:文字列(QRコード)
  int MT = 40;      // max_turn(-1の時はh*w/2)
  int DEG = -90;      // 盤面を時計回りに回転する [-90, 0, 90, 180] 赤:90, 青:-90
  int COL = BLUE;    // 自分の色選択 RED:赤, BLUE:青
  game(CG, MA, MT, B, DEG, COL);
}
/*--------------------------------------------------------------------------*/




void game(int CG, int MA, int MT, int B, int DEG, int COL){
  // 変数代入
  BoardInfo info = create::get_board(B, DEG, COL);
  h = info.h, w = info.w;
  rep(i,4){pos[i] = info.pos[i];}
  number = info.number;
  color = info.color;
  // 環境選択
  if(MT <= 0)MT = h*w/2;
  if(CG == CUI)game_CUI(MT);
  if(CG == GUI)game_GUI(MA, MT);
}


// CUI
void game_CUI(int MT){
  // 初期化
  Board board(h, w, pos, number, color);
  const int n = MT;
  PLAYER1 player1(RED, n);
  PLAYER2 player2(BLUE, n);
  printf("created (%lld, %lld) board\n", h, w);
  board.print_board();
  
  // ゲーム進行
  vector<int> isEnd(2);
  while(board.history.size() < n){
    vector<int> vec[2];
    player1.get_act(board, vec[0], isEnd[0]);
    player2.get_act(board, vec[1], isEnd[0]);
    printf("\nturn%lld: ", (int)(board.history.size()+1));
    select_disp(vec);
    board.move(vec);
    board.print_board();
  }
  
  // const int MAX = 100000;
  // // const int MAX = 100000000;
  // // const int MAX = 1;
  // printf("started\n");
  // clock_t start = clock();
  // srand((unsigned int)time(NULL));
  // vi vec[2];
  // rep(i,2)vec[i] = vi{rand()%9, 0LL, rand()%9, 0LL};
  // rep(loop,MAX){
  //   board.move(vec);
  //   board.undo(1);
  //   // board.calc_score(RED);
  //   // board.move_sort(10, RED);
  //   // board.brain(vec);
  // }
  // cout << clock()-start << endl;
}


// GUI
void game_GUI(int MA, int MT){
  // 初期化
  Board board(h, w, pos, number, color);
  int max_turn = MT;
  PLAYER1 player1(RED, max_turn);
  PLAYER2 player2(BLUE, max_turn);
  printf("created (%lld, %lld) board\n", h, w);
  board.print_board();
  vector<int> vec[2], isEnd(2);
  vector<thread> th(2);
  th[0] = thread(&PLAYER1::get_act, &player1, ref(board), ref(vec[0]), ref(isEnd[0]), 1);
  th[1] = thread(&PLAYER2::get_act, &player2, ref(board), ref(vec[1]), ref(isEnd[1]), 1);
  clock_t start = clock();
  
  // サーバーとの通信開始
  client::connect_server();
  client::send_message(board.get_init_str());
  Sleep(1000);
  client::send_message(board.get_state_str());
  struct ColorChange{bool exist;int player, y, x;};
  ColorChange Col;Col.exist = false;
  
  // ゲームループ
  while(true){
    if((int)(board.history.size()) == max_turn)break;
    if(MA == AUTO)printf("\nturn:%lld\n", (int)(board.history.size()));
    Sleep(100);
    string str = client::get_message();
    // predict送信
    if(str == "" and MA == MANUAL){
      if(clock()-start < 1000)continue;
      start = clock();
      client::send_message(board.get_predict_str(vec));
      continue;
    }
    if(str != "")cout << str << endl;
    // 通信切断(ゲーム終了)
    if(str[13] == '1')break;
    
    if(str[13] == '4'){
      int size = str.size();
      int y = 0, x = 0, i = 15;
      while(str[i] != ' '){y = y*10+str[i]-'0';i++;}i++;
      for(i;i < size-1;i++){x = x*10+str[i]-'0';}
      bool change_flag = false;
      if(Col.exist){
        board.set_color(y*w+x, EMPTY);
        board.set_color(y*w+x, board.color4[Col.player]);
        board.pos[Col.player] = y*w+x;
        Col.exist = false;
        change_flag = true;
      }
      rep(i,4)if(board.pos[i] == y*w+x and change_flag == false){
        Col = ColorChange{true, i, y, x};
        Col.exist = true;
        change_flag = true;
      }
      if(change_flag == false){
        if(board.color[y*w+x] == EMPTY){board.set_color(y*w+x, RED);}
        else if(board.color[y*w+x] == RED){board.set_color(y*w+x, EMPTY);board.set_color(y*w+x, BLUE);}
        else if(board.color[y*w+x] == BLUE){board.set_color(y*w+x, EMPTY);}
        change_flag = true;
      }
      printf("%lld %lld\n", board.calc_score(RED), board.calc_score(BLUE));
      client::send_message(board.get_state_str());
      printf("(y, x) = %lld %lld\n", y, x);
    }
    
    // thread停止
    if(str[13] == '0' or str[13] == '3' or MA == AUTO){
      if(MA == MANUAL){rep(i,2)isEnd[i] = 1;}
      rep(i,2)th[i].join();
      rep(i,2)isEnd[i] = 0;
    }
    // 行動
    if(str[13] == '0' or MA == AUTO){
      if(MA == AUTO)board.move(vec);
      else board.move_str(str);
    }
    // 1手戻る
    if(str[13] == '3'){
      board.undo(1);
    }
    // thread再開
    if(str[13] == '0' or str[13] == '3' or MA == AUTO){
      board.print_board();
      client::send_message(board.get_state_str());
      th[0] = thread(&PLAYER1::get_act, &player1, ref(board), ref(vec[0]), ref(isEnd[0]), 1);
      th[1] = thread(&PLAYER2::get_act, &player2, ref(board), ref(vec[1]), ref(isEnd[1]), 1);
      start = clock();
    }
    
  }
  // 終了
  printf("disconnected\n");
  rep(i,2)isEnd[i] = 1;
  rep(i,2)th[i].join();
  client::disconnect_server();
}

// 選択表示
void select_disp(vi vec[2]){
  printf("selected\n");
  printf("player1:(%lld, %lld), ", vec[0][0], vec[0][1]);
  printf("player2:(%lld, %lld)\n", vec[0][2], vec[0][3]);
  printf("player3:(%lld, %lld), ", vec[1][0], vec[1][1]);
  printf("player4:(%lld, %lld)\n", vec[1][2], vec[1][3]);
}








