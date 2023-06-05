#include "header.h"
#include "CreateBoard.h"

/*
8 11:-2 1 0 1 2 0 2 1 0 1 -2:1 3 2 -2 0 1 0 -2 2 3 1:1 3 2 1 0 -2 0 1 2 3 1:2 1 1 2 2 3 2 2 1 1 2:2 1 1 2 2 3 2 2 1 1 2:1 3 2 1 0 -2 0 1 2 3 1:1 3 2 -2 0 1 0 -2 2 3 1:-2 1 0 1 2 0 2 1 0 1 -2:2 2:7 10:
*/
/*
12 12:-2 5 13 0 11 7 7 11 0 13 5 -2:0 16 6 1 9 7 7 9 1 6 16 0:1 -15 -11 9 3 6 6 3 9 -11 -15 1:12 14 15 8 0 12 12 0 8 15 14 12:12 1 -8 13 5 -15 -15 5 13 -8 1 12:13 -14 7 3 -12 4 4 -12 3 7 -14 13:6 1 7 0 5 -5 -5 5 0 7 1 6:13 -1 0 11 -10 -5 -5 -10 11 0 -1 13:10 14 6 -6 12 1 1 12 -6 6 14 10:15 14 7 4 6 8 8 6 4 7 14 15:13 11 -7 -6 2 -12 -12 2 -6 -7 11 13:11 0 6 0 3 11 11 3 0 6 0 11:4 2:6 1:
*/
/*
12 12:-2 5 13 0 11 7 7 11 0 13 5 -2:0 16 6 1 9 7 7 9 1 6 16 0:1 -15 -11 9 3 6 6 3 9 -11 -15 1:12 14 15 8 0 12 12 0 8 15 14 12:12 1 -8 13 5 -15 -15 5 13 -8 1 12:13 -14 7 3 -12 4 4 -12 3 7 -14 13:6 1 7 0 5 -5 -5 5 0 7 1 6:13 -1 0 11 -10 -5 -5 -10 11 0 -1 13:10 14 6 -6 12 1 1 12 -6 6 14 10:15 14 7 4 6 8 8 6 4 7 14 15:13 11 -7 -6 2 -12 -12 2 -6 -7 11 13:11 0 6 0 3 11 11 3 0 6 0 11:4 2:6 1: [3 10:5 11]
*/

// ボードを作る
// 引数(k = 0): サンプルボード
// 引数(k = 1): ランダムボード
// 引数(k = 2): 文字列インプット
BoardInfo create::get_board(int k, int deg,int col){
  srand((unsigned int)time(NULL));
  
  // 変数宣言
  BoardInfo info;
  int h, w, pos[4];
  vi number, color;
  
  // サンプルボード
  if(k == 0){
    h = 8, w = 11;
    int Pos[4] = {(2-1)*w+(10-1), (7-1)*w+(2-1), (2-1)*w+(2-1), (7-1)*w+(10-1)};
    vector<int> Number{
    -2, 1, 0, 1, 2, 0, 2, 1, 0, 1, -2,
    1, 3, 2, -2, 0, 1, 0, -2, 2, 3, 1,
    1, 3, 2, 1, 0, -2, 0, 1, 2, 3, 1,
    2, 1, 1, 2, 2, 3, 2, 2, 1, 1, 2,
    2, 1, 1, 2, 2, 3, 2, 2, 1, 1, 2,
    1, 3, 2, 1, 0, -2, 0, 1, 2, 3, 1,
    1, 3, 2, -2, 0, 1, 0, -2, 2, 3, 1,
    -2, 1, 0, 1, 2, 0, 2, 1, 0, 1, -2};
    rep(i,4)pos[i] = Pos[i];
    number = Number;
  }
  
  // ランダムボード
  if(k == 1){
    h = rand()%6+7; // [7,12]
    int lb = (80+h-1)/h;  // 80 <= lb*h
    w = rand()%(12-lb+1)+lb;  // [lb,12]
    vi vec;
    rep(i,h*w){
      int num = rand()%17;
      number.push_back(rand()%10 < 2 ? -num : num);
      if(h%2 == 1 and i/w == h/2)continue;
      if(w%2 == 1 and i%w == w/2)continue;
      vec.push_back(i);
    }
    int r1 = rand()%vec.size(), r2 = rand()%(vec.size()-1);
    pos[0] = vec[r1];vec.erase(vec.begin()+r1);
    pos[1] = vec[r2];
    if(rand()%2 == 0){  // y軸
      rep(i,2){
        int y = pos[i]/w, x = pos[i]%w;
        pos[i+2] = y*w+(w-x-1);
      }
      rep(i,h)rep(j,w){
        if(j < (w+1)/2)continue;
        number[i*w+j] = number[i*w+(w-j-1)];
      }
    }else{    // x軸
      rep(i,2){
        int y = pos[i]/w, x = pos[i]%w;
        pos[i+2] = (h-y-1)*w+x;
      }
      rep(i,h)rep(j,w){
        if(i < (h+1)/2)continue;
        number[i*w+j] = number[(h-i-1)*w+j];
      }
    }
  }
  
  // 文字列インプット
  if(k == 2){
    string str;
    getline(cin, str);
    str += ":";
    int p = 0, f = 1;
    h = get_num(str, p), w = get_num(str, p);
    rep(i,h)rep(j,w)number.push_back(get_num(str, p));
    rep(i,4)pos[i] = (get_num(str, p)-1)*w+(get_num(str, p)-1);
    if(100 <= pos[2] or 100 <= pos[3]){ // y軸対称
      rep(i,2)pos[i+2] = (pos[i]/w)*w+(w-pos[i]%w-1);
    }
    rep(i,h)if(number[i*w] != number[(h-i-1)*w])f = 0;
    if(f or pos[0] == pos[2] or pos[1] == pos[3]){  // x軸対称
      rep(i,2)pos[i+2] = (h-pos[i]/w-1)*w+(pos[i]%w);
    }
  }
  
  // 盤面回転
  int cnt_r = (deg+360*4)%360/90;
  rep(i,cnt_r)rotate_board(h, w, pos, number);
  
  // 色選択
  if(col == BLUE){rep(i,2)swap(pos[i], pos[i+2]);}
  
  // 変数セット
  color.resize(h*w);
  color[pos[0]] = color[pos[1]] = RED;
  color[pos[2]] = color[pos[3]] = BLUE;
  info.h = h, info.w = w;
  rep(i,4){info.pos[i] = pos[i];}
  info.number = number;
  info.color = color;
  return info;
}

int create::get_num(string str, int &p){
  int res = 0, n = str.size();
  while(p < n and !isdigit(str[p]) and str[p] != '-')p++;
  if(n <= p)return 100+1;
  int s = p;
  while(p < n and (isdigit(str[p]) or str[p] == '-'))p++;
  return atoll(str.substr(s, p-s).c_str());
}

void create::rotate_board(int &h, int &w, int pos[4], vi &number){
  vi vec;
  rep(j,w)drep(i,h-1,0)vec.push_back(number[i*w+j]);
  number = vec;
  rep(i,4){
    int y = pos[i]/w, x = pos[i]%w;
    pos[i] = (x)*h+(h-y-1);
  }
  swap(h, w);
}

