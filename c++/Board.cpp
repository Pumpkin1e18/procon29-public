#include "Board.h"
#include "header.h"

// [0, (2^32)-1] の一様分布整数を生成
uint32_t get_rand() {
    static mt19937 mt32((uint)time(NULL));
    return mt32();
}

// 初期化
Board::Board(){
  // pass
}

// 初期化
Board::Board(int H, int W, int Pos[4], vi num, vi Color){
  init(H, W, Pos, num, Color);
}

// 初期化処理
void Board::init(int H, int W, int Pos[4], vi num, vi Color){
  h = H;w = W;used.resize(h*w);number = num;color = Color;
  eigenvalue = 0;rand_max = 1;
  rep(i,6)zip[i] = 0;
  rep(i,29)rand_max *= 2;
  rep(i,2+4){rep(j,h*w)random_table[i].push_back(get_rand()%rand_max);}
  // 盤面情報初期化
  rep(i,4){pos[i] = Pos[i];}score[0] = score[1] = 0;
  rep(i,H*W){
    set_zip_bit(i, color[i]);
    if(color[i] == RED)score[0] += number[i];
    if(color[i] == BLUE)score[1] += number[i];
  }
  com.update(pos, zip, eigenvalue+history.size()%8*rand_max);
  // 変換変数初期化
  color4[0] = color4[1] = RED;
  color4[2] = color4[3] = BLUE;
  color2[RED] = 0;color2[BLUE] = 1;
  color3[EMPTY] = 0;color3[RED] = 1;color3[BLUE] = 2;
  int DV4[] = {-W, -1, 1, W}, DV9[] = {-W-1, -W, -W+1, -1, 0, 1, W-1, W, W+1};
  rep(i,4){dv4[i] = DV4[i];}
  rep(i,9){dv9[i] = DV9[i];}
}

// ボードの表示
void Board::print_board(){
  vector<int> disp = color;
  disp[pos[0]] = disp[pos[1]] = PLAYER_RED;
  disp[pos[2]] = disp[pos[3]] = PLAYER_BLUE;
  rep(i,h){
    rep(i,w)printf("------");printf("\n");
    rep(j,w){
      printf("%3lld|", number[i*w+j]);
      if(disp[i*w+j] == RED)printf("■");
      else if(disp[i*w+j] == BLUE)printf("□");
      else if(disp[i*w+j] == PLAYER_RED)printf("●");
      else if(disp[i*w+j] == PLAYER_BLUE)printf("〇");
      else printf("　");
    }
    printf("\n");
  }
  rep(i,w)printf("------");printf("\n");
  int point[2] = {calc_score(RED), calc_score(BLUE)};
  int area[2] = {point[0]-score[0], point[1]-score[1]};
  printf("■RED■:%lld (%lld), ", point[0], area[0]);
  printf("□BLUE□:%lld (%lld), ", point[1], area[1]);
  printf("DIFF:%lld (%lld)\n", llabs(point[0]-point[1]), llabs(area[0]-area[1]));
  rep(i,4)printf("player%lld (%lld, %lld)\n", i+1, pos[i]/w+1,pos[i]%w+1);
  printf("\n");
}

// bitの表示
void Board::print_zip(){
  vi v[3];
  int tmp[6];
  rep(i,6)tmp[i] = zip[i];
  rep(i,3)rep(j,5*w){
    v[i].push_back(tmp[i]%2);
    tmp[i] = tmp[i]/2;
  }
  rep(y,h){
    rep(x,w){
      int id = y/5, bit = y*w+x-id*w*5;
      printf("%lld", v[id][bit]);
    }
    printf("\n");
  }
}

void Board::set_zip_bit(int Pos, int Color){
  int id = Pos/w/5, mod = Pos-id*w*5, shift = 1LL<<mod;
  if(Color == RED)zip[id] += shift;
  else if(Color == BLUE)zip[3+id] += shift;
  else if(Color == EMPTY){
    if(zip[id] & shift)zip[id] -= shift;
    if(zip[3+id] & shift)zip[3+id] -= shift;
  }
}

// マスに色をセットする
void Board::set_color(int Pos, int Color){
  // 色を付ける場合は無色にしておく
  if(Color == RED and color[Pos] != RED){
    eigenvalue ^= random_table[0][Pos];
    score[0] += number[Pos];
    set_zip_bit(Pos, RED);
  }else if(Color == BLUE and color[Pos] != BLUE){
    eigenvalue ^= random_table[1][Pos];
    score[1] += number[Pos];
    set_zip_bit(Pos, BLUE);
  }else if(Color == EMPTY and color[Pos] != EMPTY){
    if(color[Pos] == RED){
      eigenvalue ^= random_table[0][Pos];
      score[0] -= number[Pos];
    }else{
      eigenvalue ^= random_table[1][Pos];
      score[1] -= number[Pos];
    }
    set_zip_bit(Pos, EMPTY);
  }
  color[Pos] = Color;
}

// 領域ポイントを数える
int Board::dfs(int now){
  if(used[now])return 0;
  used[now] = 1;
  int sum = 0, flag = 0;
  rep(i,4){
    int nxt = now+dv4[i];
    if(nxt < 0 or h*w <= nxt or llabs(nxt%w-now%w) > 1){flag = 1;continue;}
    int res = dfs(nxt);
    if(res == -1)flag = 1;
    sum += res;
  }
  if(flag)return -1;
  return sum+llabs(number[now]);
}

// 得点を数える
int Board::calc_score(int Color){
  int add = 0;
  fill(used.begin(), used.end(), 0);
  rep(i,h*w){if(color[i] == Color)used[i] = 1;}
  rep(i,h*w){if(!used[i])add += max(0LL, dfs(i));}
  int point = (Color == RED ? score[0] : score[1]);
  return point+add;
}

// 9近傍に相手がいるかどうか
bool Board::adjacent(int id, int Color){
  int base = (Color == RED ? 2 : 0);
  if(Color == BLUE)id += 2;
  rep(i,2){
    int dx = llabs(pos[id]%w-pos[base+i]%w);
    int dy = llabs(pos[id]/w-pos[base+i]/w);
    if(max(dx, dy) <= 1LL)return true;
  }
  return false;
}

// スコアが同じときペアとの距離が遠くなる方に加点
double Board::calc_value(int id, int act, int Color){
  int id_p = (id%2 ? id-1 : id+1);
  int now = pos[id], nxt = pos[id]+dv9[act], now_p = pos[id_p];
  if(nxt < 0 or h*w <= nxt or llabs(now%w-nxt%w) > 1)return 0;
  int nxt_d = llabs(nxt/w-now_p/w) + llabs(nxt%w-now_p%w);
  int now_d = llabs(now/w-now_p/w) + llabs(now%w-now_p%w);
  int d[] = {-w, -1, 1, w}, add = 0;
  rep(i,4){
    int dd = nxt+d[i];
    if(dd < 0 or h*w <= dd or llabs(nxt%w-dd%w) > 1)continue;
    if(color[dd] == Color)add--;
    if(color[dd] == -Color)add++;
  }
  return 0.1*(nxt_d-now_d)+add;
}

// 次の1手をソートする
vector<P> Board::move_sort(int n, int Color, int isBeam){
  typedef pair<double, int> Pd;
  typedef pair<double, P> PP;
  priority_queue<PP> q;
  vector<Pd> mov[2];
  vector<P> vec;
  int now[2] = {pos[color2[Color]*2], pos[color2[Color]*2+1]};
  int now_p[2] = {pos[color2[-Color]*2], pos[color2[-Color]*2+1]};
  // 価値代入
  rep(i,2)mov[i].resize(9);
  rep(i,2)rep(j,9){
    int nxt = now[i]+dv9[j], b = (Color==BLUE)*2, id = i+b;
    double value = calc_value(id, j, Color);
    if(nxt < 0 or h*w <= nxt or llabs(nxt%w-now[i]%w) > 1)value += -20;
    else if(isBeam and (nxt == now_p[0] or nxt == now_p[1]))value += -20;
    else if(nxt == pos[(b+2)%4] or nxt == pos[(b+3)%4])value += number[nxt]-5;
    else if(color[nxt] == -Color)value += number[nxt]+2;
    else if(color[nxt] == -Color and adjacent(i, Color))value += number[nxt]+5;
    else if(color[nxt] != Color)value += number[nxt];
    else if(now[i] == nxt)value += -1;
    else if(number[nxt] < 0)value += -number[nxt]+5;
    else value += 0;
    mov[i][j] = Pd(value, j);
  }
  // 価値が降順で取り出す
  sort(mov[1].begin(), mov[1].end(), greater<Pd>());
  rep(i,9)q.push(PP(mov[0][i].fi+mov[1][0].fi, P(i, 0)));
  while(vec.size() < n){
    P p = q.top().se;q.pop();
    int v1 = p.fi, v2 = mov[1][p.se].se;
    int nxt1 = now[0]+dv9[v1], nxt2 = now[1]+dv9[v2];
    int b1 = (color[nxt1] == Color and number[nxt1] < 0);
    int b2 = (color[nxt2] == Color and number[nxt2] < 0);
    if(nxt1 != nxt2)vec.push_back(P(v1*9+v2, b1*2+b2));
    if(p.se < 8)q.push(PP(mov[0][p.fi].fi+mov[1][p.se+1].fi, P(p.fi, p.se+1)));
  }
  return vec;
}

// 行動
void Board::move(const vi (&vec)[2]){
  History his{{pos[0],pos[1],pos[2],pos[3]}, {score[0],score[1]}, eigenvalue};
  int nxt[4], rev[4] = {}, cnt[12*12] = {};
  rep(i,4){ // 合法な動きか判定してひっくり返すかどうか見る
    nxt[i] = pos[i]+dv9[vec[i/2][i%2*2]];
    if(nxt[i] < 0 or h*w <= nxt[i])nxt[i] = pos[i];
    if(llabs(nxt[i]%w-pos[i]%w) > 1)nxt[i] = pos[i];
    cnt[nxt[i]]++;
    if(color[nxt[i]] == -color4[i])rev[i] = 1;
    if(color[nxt[i]] != EMPTY and vec[i/2][i%2*2+1])rev[i] = 1;
    his.past[2*i] = P(pos[i], color[pos[i]]);
    his.past[2*i+1] = P(nxt[i], color[nxt[i]]);
  }
  history.push(his);
  
  rep(i,4){ // 移動できない人たちの処理
    if(cnt[nxt[i]] <= 1 and rev[i])set_color(nxt[i], EMPTY);
    if(cnt[nxt[i]] > 1 or rev[i])nxt[i] = pos[i];
  }
  rep(i,4){ // 移動
    if(pos[i] != nxt[i]){
      eigenvalue ^= random_table[i+2][pos[i]];
      eigenvalue ^= random_table[i+2][nxt[i]];
    }
    pos[i] = nxt[i];
    set_color(nxt[i], color4[i]);
  }
  com.update(pos, zip, eigenvalue+history.size()%8*rand_max);
}


// 1手戻る
void Board::undo(int n){
  int size = min((int)history.size(), n);
  if(size == 0)return;
  rep(i,size){
    History his = history.top();history.pop();
    rep(j,8)set_color(his.past[j].fi, his.past[j].se);
    if(i == size-1){
      rep(j,4){pos[j] = his.pos[j];}
      rep(j,2){score[j] = his.score[j];}
      eigenvalue = his.eigenvalue;
    }
  }
  com.update(pos, zip, eigenvalue+history.size()%8*rand_max);
}


void Board::brain(vi vec[2]){
  int cntup = 0;
}



// Unityとの通信のためにデータを変形する
// [FromPython]: 0 h w number[h*w] pos[4]         初期化
// [FromPython]: 1 color[h*w] pos[4] score[2]         ゲーム進行
// [FromPython]: 2 [[v1[i], b1[i]], ...]      最善手(only first)予測

// 初期盤面の文字列を返す
string Board::get_init_str(){
  string str = "[FromPython]: 0 ";
  str += to_string(h)+" ";
  str += to_string(w)+" ";
  rep(i,h*w)str += to_string(number[i])+" ";
  rep(i,4)str += to_string(pos[i]/w)+" " + to_string(pos[i]%w)+" ";
  return str;
}

// それぞれのマスの色とプレイヤーの位置を返す
string Board::get_state_str(){
  string str = "[FromPython]: 1 ";
  rep(i,h*w)str += to_string(color3[color[i]])+" ";
  rep(i,4)str += to_string(pos[i]/w)+" " + to_string(pos[i]%w)+" ";
  str += to_string(calc_score(RED))+" ";
  str += to_string(calc_score(BLUE))+" ";
  return str;
}

// プレイヤーのpredictの文字列を返す
string Board::get_predict_str(vi vec[2]){
  string str = "[FromPython]: 2 ";
  rep(i,2)rep(j,4)str += to_string(vec[i][j])+" ";
  return str;
}

// Unityからの文字列を受け取って行動する
void Board::move_str(string str){
  int p = 15;
  vi vec[2];
  rep(i,2)rep(j,4){
    vec[i].push_back(str[p]-'0');
    p += 2;
  }
  move(vec);
}







