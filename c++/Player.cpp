#include "Board.h"
#include "Player.h"
#include "header.h"

// Random
/*--------------------------------------------------------------------------*/
PlayerRandom::PlayerRandom(int ROLE, int MAX_TURN){  // 初期化
  role = ROLE;
}

void PlayerRandom::get_act(Board &BOARD, vi &vec, int &IsEnd, int CG){  // 行動取得
  srand((unsigned int)time(NULL));
  vec = vi{rand()%9, 0LL, rand()%9, 0LL};
  return;
}
/*--------------------------------------------------------------------------*/




// Greedy
/*--------------------------------------------------------------------------*/
PlayerGreedy::PlayerGreedy(int ROLE, int MAX_TURN){  // 初期化
  role = ROLE;
  width = 5;
}

void PlayerGreedy::get_act(Board &BOARD, vi &vec, int &IsEnd, int CG){  // 行動取得
  srand((unsigned int)time(NULL));
  vector<P> v = BOARD.move_sort(width, role);
  rep(i,v.size())printf("(%lld, %lld) ", v[i].fi/9, v[i].fi%9);
  printf("\n");
  P pos = v[rand()%width];
  vec = vi{pos.fi/9, pos.se/2, pos.fi%9, pos.se%2};
  return;
}
/*--------------------------------------------------------------------------*/



// Human
/*--------------------------------------------------------------------------*/
PlayerHuman::PlayerHuman(int ROLE, int MAX_TURN){  // 初期化
  role = ROLE;
}

void PlayerHuman::get_act(Board &BOARD, vi &vec, int &IsEnd, int CG){ // 行動取得
  if(CG == GUI){vec = vi{-1, -1, -1, -1};return;}
  string str;
  while(true){
    printf("input:");getline(cin, str);
    str += " ";
    vector<int> v;
    int num = 0;
    if(str.substr(0, 4) == "undo" or str.substr(0, 4) == "UNDO"){ // undo
      repi(i,4,str.size()){
        if(0 <= str[i]-'0' and str[i]-'0' <= 9)num = num*10+str[i]-'0';
        if(200LL < num)break;
      }
      BOARD.undo(max(num, 1LL));
      BOARD.print_board();
      continue;
    }
    rep(i,str.size())if(0 <= str[i]-'0' and str[i]-'0' <= 9){ // put
      if(v.size() == 4)break;
      v.push_back(str[i]-'0');
    }
    if(v.size() == 2){
      if(v[0] <= 9 and v[1] <= 9){
        vec = vi{v[0], 0LL, v[1], 0LL};break;
      }
    }else if(v.size() == 4){
      v[1] = (int)(!!v[1]);v[3] = (int)(!!v[3]);
      if(v[0] <= 9 and v[2] <= 9){
        vec = v;break;
      }
    }
    printf("invalid operation\n");
  }
  return;
  
}
/*--------------------------------------------------------------------------*/



// AlphaBeta
/*--------------------------------------------------------------------------*/
PlayerAlphaBeta::PlayerAlphaBeta(int ROLE, int MAX_TURN){  // 初期化
  role = ROLE;max_turn = MAX_TURN;
  prev_score = 0;
  width = 8;
  max_depth = 8;  // ここは実質関係ない
}

int PlayerAlphaBeta::get_score(int f){
  leaf_total++;
  int point[2] = {board.calc_score(role), board.calc_score(-role)};
  int res = point[0]-point[1];
  if(f == 0)return res;
  
  int add[2] = {}, dis[2] = {}, h = board.h, w = board.w, pos[4];
  rep(i,4)pos[i] = board.pos[i];
  rep(i,2){dis[i] += llabs(pos[2*i]/w-pos[2*i+1]/w)+llabs(pos[2*i]%w-pos[2*i+1]%w);}
  rep(i,4)rep(y,3)rep(x,3){
    int Color = board.color4[i];
    int yy = (pos[i]/w)+(y-1), xx = (pos[i]%w)+(x-1);
    if(yy < 0 or h <= yy or xx < 0 or w <= xx){
      if(board.history.size() < board.h*board.w/6)add[i/2] += 1;
    }else if(board.color[yy*w+xx] == Color)add[i/2] += -2;
    else add[i/2] += 1;
  }
  add[role==BLUE] += (point[0]-prev_score)/2;
  
  int Dis = (role == RED ? dis[0]-dis[1] : dis[1]-dis[0]);
  int Add = (role == RED ? add[0]-add[1] : add[1]-add[0]);
  int sup = (Add+Dis/2)/4;
  add_min = min(add_min, sup);
  add_max = max(add_max, sup);
  // add_min = min(add_min, res);
  // add_max = max(add_max, res);
  
  add_total += sup;
  return res+sup;
}

int PlayerAlphaBeta::alphabeta(int alpha, int beta, int color, int depth, P mov){
  if(color == role){
    if(hash_cnt[board.com.seed])hash_total++;
    hash_cnt[board.com.seed]++;
    node_cnt[depth/2]++;
    if(table.find(board.com) != table.end()){
      same_cnt[depth/2]++;
      int value = table[board.com].value;
      if(depth and value != inf and table[board.com].v[0].size())return value;
    }
    if((int)board.history.size() == max_turn)return table[board.com].value = get_score(0);
    if(depth == max_depth)return table[board.com].value = get_score(1);
  }
  
  int idx = 0;
  vi pos;
  vector<P> v;
  Memo &memo = table[board.com];
  if(color == role and memo.v[0].size() == 0){
    memo.v[0] = board.move_sort(width, color);
    memo.v[1] = board.move_sort(width, -color);
  }
  v = memo.v[color==-role];
  rep(i,v.size())pos.push_back(v[i].fi);
  
  if(color == role){  // 自分の手番
    rep(i,width){
      if(*isEnd)return alpha;
      int res = alphabeta(alpha, beta, -color, depth+1, P(pos[i], v[i].se));
      if(depth == 0)printf("(%lld, %lld){%lld} ", pos[i]/9, pos[i]%9, res);
      if(depth == 0 and alpha < res)best = P(pos[i], v[i].se);
      if(alpha < res){alpha = res;idx = i;}
      if(alpha >= beta)break;
    }
    drep(j,idx,1)swap(memo.v[0][j-1], memo.v[0][j]);
    memo.value = alpha;
    if(depth == 0)printf("alpha = %lld\n", alpha);
    return alpha;
  }else{  // 相手の手番
    rep(i,width){
      if(*isEnd)return beta;
      vi vec[2]{{mov.fi/9, mov.se/2, mov.fi%9, mov.se%2}, 
                {pos[i]/9, v[i].se/2, pos[i]%9, v[i].se%2}};
      if(role == BLUE)swap(vec[0], vec[1]);
      board.move(vec);
      int res = alphabeta(alpha, beta, -color, depth+1, P(0, 0));
      board.undo(1);
      if(beta > res){beta = res;idx = i;}
      if(alpha >= beta)break;
    }
    drep(j,idx,1)swap(memo.v[1][j-1], memo.v[1][j]);
    return beta;
  }
}

void PlayerAlphaBeta::get_act(Board &BOARD, vi &vec, int &IsEnd, int CG){ // 行動取得
  board = BOARD;
  rep(i,20){same_cnt[i] = 0;node_cnt[i] = 0;}
  table.clear();
  isEnd = &IsEnd;
  leaf_total = add_total = 0;
  add_min = inf, add_max = -inf;
  hash_total = 0;
  hash_cnt.clear();
  vec = vi{-1, -1, -1, -1};
  
  prev_score = board.calc_score(role);
  int alpha = -INF, beta = INF;
  clock_t start = clock();
  max_depth = 6;
  alphabeta(alpha, beta, role, 0, P(0, 0));
  for(auto it = table.begin();it != table.end();++it)it->se.value = inf;
  max_depth = 8;
  alphabeta(alpha, beta, role, 0, P(0, 0));
  
  for(auto it = table.begin();it != table.end();++it)it->se.value = inf;
  max_depth = 10;
  alphabeta(alpha, beta, role, 0, P(0, 0));
  
  table.clear();
  vec = vi{best.first/9, best.second/2, best.first%9, best.second%2};
  
  // 表示
  int same_total = 0, node_total = 0;
  rep(i,max_depth+1){same_total += same_cnt[i];node_total += node_cnt[i];}
  printf("same_cnt: %lld ( ", same_total);
  rep(i,max_depth/2+1)printf("%lld ", same_cnt[i]);printf(")\n");
  printf("node_cnt: %lld ( ", node_total);
  rep(i,max_depth/2+1)printf("%lld ", node_cnt[i]);printf(")\n");
  printf("same_hash_cnt: %lld\n", hash_total);
  printf("add_min: %lld add_max: %lld\n", add_min, add_max);
  printf("add_average: %lld\n", add_total/leaf_total);
  printf("AlphaBeta finished in ");cout << clock()-start << "ms" << endl;
  return;
}
/*--------------------------------------------------------------------------*/

