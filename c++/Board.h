#include "header.h"

#ifndef PBOARD
#define PBOARD

// class for hash
class Compact{
public:
  uint seed;  // size%8も含めたseed値を渡すこと: 16depthの以上は対応してない
  int pos[4], zip[6];
	Compact(){}
  void update(int (&Pos)[4], int (&Zip)[6], uint Seed){
    rep(i,4)pos[i] = Pos[i];
    rep(i,6)zip[i] = Zip[i];
    seed = Seed;
  }
  bool operator==(const Compact& right) const{
    const Compact &left = *this;
    rep(i,4)if(left.pos[i] != right.pos[i])return false;
    rep(i,6)if(left.zip[i] != right.zip[i])return false;
    return true;
  }
  struct Hash{
      typedef size_t result_type;
      size_t operator()(const Compact& key) const{
        return key.seed;
      }
  };
};

class Board{
public:
  struct History{int pos[4], score[2], eigenvalue;P past[8];};
  stack<History> history;
  Compact com;
  int h, w, pos[4], score[2], dv4[4], dv9[9], zip[6];
  vector<int> number, color, used;
  uint eigenvalue, rand_max;
  vector<uint> random_table[6];
  unordered_map<int, int> color2, color3, color4;
  
  Board();
  Board(int H, int W, int Pos[4], vi num, vi Color);
  void init(int H, int W, int Pos[4], vi num, vi Color);
  void print_board();
  void print_zip();
  
  void set_zip_bit(int Pos, int Color);
  void set_color(int Pos, int Color);
  int dfs(int now);
  int calc_score(int Color);
  bool adjacent(int id, int Color);
  double calc_value(int id, int act, int Color);
  vector<P> move_sort(int n, int Color, int isBeam = 0);
  void move(const vi (&vec)[2]);
  void undo(int n);
  
  // 計測用
  void brain(vi vec[2]);
  
  // Unityとの通信用
  string get_init_str();
  string get_state_str();
  string get_predict_str(vi vec[2]);
  void move_str(string str);
  
  bool operator==(const Board& right) const{
    const Board &left = *this;
    rep(i,4)if(left.pos[i] != right.pos[i])return false;
    rep(i,6)if(left.zip[i] != right.zip[i])return false;
    if(left.history.size() != right.history.size())return false;
    return true;
  }
  struct Hash{
      typedef size_t result_type;
      size_t operator()(const Board& key) const{
        uint seed = key.eigenvalue;
        seed += key.history.size()%8*key.rand_max;
        return seed;
      }
  };
};

struct Memo{int value = 0;vector<P> v[2];};
typedef unordered_map<Compact, Memo, Compact::Hash> Map;
// typedef unordered_map<Board, int, Board::Hash> Map;


#endif