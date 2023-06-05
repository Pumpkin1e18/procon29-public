#include "header.h"

// Memo
// ターン数(40~80)
// マスの数(80~140)
// 点数(-16~16)
// 1ターンの時間(10~20)
// 1マス(50cmx50cm)
// フィールド最大(6mx6m)
// フィールドとの距離(50cm~2m)
// テーブル(180cmx45cmx高さ70cm)


// ボード情報を格納する構造体
struct BoardInfo{int h, w, pos[4];vi number, color;};

namespace create{
  // ボードを作る
  // 引数(k = 0): サンプルボード
  // 引数(k = 1): ランダムボード
  BoardInfo get_board(int k, int deg, int col);
  
  // QRコードの情報の数字を1つ読み取る
  int get_num(string str, int &p);
  
  // 時計回りに90度回転する
  void rotate_board(int &h, int &w, int pos[4], vi &number);
};




