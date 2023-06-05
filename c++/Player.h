#include "Board.h"
#include "header.h"

class PlayerRandom{
public:
  Board board;
  int role;
  PlayerRandom(int ROLE, int MAX_TURN);  // 初期化
  void get_act(Board &BOARD, vi &vec, int &IsEnd, int CG = 0);  // 行動取得
};

class PlayerGreedy{
public:
  Board board;
  int role, width;
  PlayerGreedy(int ROLE, int MAX_TURN);  // 初期化
  void get_act(Board &BOARD, vi &vec, int &IsEnd, int CG = 0);  // 行動取得
};

class PlayerHuman{
public:
  Board board;
  int role;
  PlayerHuman(int ROLE, int MAX_TURN);  // 初期化
  void get_act(Board &BOARD, vi &vec, int &IsEnd, int CG = 0);  // 行動取得
};

// typedef unordered_map<Board, int, Board::Hash> Map;
class PlayerAlphaBeta{
public:
  Map table;
  Board board;
  int role, width, max_depth, last, max_turn, prev_score, *isEnd;
  int hash_total, leaf_total, add_total, add_min, add_max;
  int same_cnt[20], node_cnt[20];
  unordered_map<uint, int> hash_cnt;
  P temp_best, best;
  PlayerAlphaBeta(int ROLE, int MAX_TURN);  // 初期化
  int get_score(int f);
  int alphabeta(int alpha, int beta, int color, int depth, P mov);
  void get_act(Board &BOARD, vi &vec, int &IsEnd, int CG = 0);  // 行動取得
};