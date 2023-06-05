## 概要
第29回高専プロコン競技部門「巡りマス」の府大高専のソルバーです。  
Pythonのコードはすべてc++で書き直しています。  

## 予選リーグ
|対戦相手|結果|勝敗|
|:---|:---|:---|
|松江|76-67|勝|
|鶴岡|156-59|勝|
|徳山|103-79|勝|

## 決勝リーグ
| |対戦相手|結果|勝敗|
|:---|:---|:---|:---|
|1回戦|都立(品川)|73-53|勝|
|2回戦|秋田|256-151|勝|
|準々決勝|阿南|159-169|負|

## 環境構築
動く保証はないです。

下記2つのツールをインストールする
- [MinGW-w64](http://text.baldanders.info/remark/2018/03/mingw-w64/) (threadのため)
- [GnuWin32](https://qiita.com/tokikaze0604/items/e13c04192762f8d4ec85) (makeのため)  

下記4つを順に実行する  
1. `c++/server.cpp`を`g++ -o server.exe server.cpp -lws2_32`でコンパイル・実行  
2. `Environment/Visualizer.exe`をダブルクリックで実行  
3. `c++/Interface.cpp`を`make`で実行  
4. `c++/QR_Reader.py`で読み取ったQRコードの文字列をコピペ  

※文字化けしてたら`chcp 65001`  
※QRコードのサンプルはQR_sampleにあります  
※c++版ではプレイヤーの選択は`c++/Interface.cpp`からしかできません
他設定は`c++/Interface.cpp`開いて環境設定の欄をいじってください  
あとはVisualizerで操作するだけ  

## 簡単なアルゴリズムの説明
### 探索
- 探索にはdepth8、width10のAlphaBeta探索を用いてる。  
- 葉ノードでの静的関数は、「自分の得点-相手の得点」に加え、「係数をかけた自分の得点」、「プレイヤーの周囲の色」も静的関数に加えた。  
- それぞれのノードで「盤面外への手は価値を下げる」、「相手が味方の8近傍にいたら相手のマスを取る手の価値を上げる」などの調整をした。  

### 高速化
- Nを1人のプレイヤーの次の選択肢の数として愚直にソートするとO(N*N)かかるが優先順位付きキューを用いてO(NlogN+WIDTHlogN)に抑えた。
- hash値の計算には、それぞれのマスに乱数を割り当てて一手進めるごとに色が変わったマスの数字をxorすることで次の局面のhash値を求める方法をとった。
- depth6を探索するとき、そのノードで良かった順に手をソートしてからdepth8で探索することでalphaカット、betaカットを起こりやすくした。

### 高専だよりへの掲載
全国高等専門学校 第29回プログラミングコンテスト競技部門特別賞

10月27日～10月28日に全国高等専門学校プログラミングコンテストという高専生だけで競い合うプログラミングコンテストの競技部門に参加してきて特別賞をいただきました。  
今年の競技はマス目に区切られたフィールド上で、1名の司令塔がA4トランプやハンドサインを使ってフィールド上を移動する２名のエージェントに指示を出して、できるだけ多くの陣地を占有する陣取りゲームでした。  
高専プロコンは他のプロコンと違い、良くも悪くも人が介在します。「人とコンピュータでどっちの方が得意か」、「できるだけ素早く入力、表示を見やすく」などを考えてプログラムを作るのは今までに経験がなく、作っててとても楽しかったです。  
プログラムはいろいろ試して最終的にはアルファベータ法というアルゴリズムで落ち着きましたがこれでも人間よりはるかに強いものは作れなかったので人間とコンピュータで役割分担しました。本番の予選リーグでは指示がうまく伝わらないことが何度もありましたが決勝トーナメントでは上手くいきました。  
最後はあと1歩で3位入賞というところで主催校阿南に負け、ベスト8に終わりました。特別賞が取れたのはカメラを使ってフィールドの状態をディスプレイに表示する工夫が評価されたんだと思います。今後参加する機会があれば今回より良い順位を取りたいです。

### 参加記
https://pumpkin1e18.hatenablog.com/entry/2018/11/01/221725?_ga=2.137702771.212017194.1541066954-1212305917.1503252936
