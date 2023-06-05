#ifndef HEADER
#define HEADER

// game define
#define EMPTY 0
#define RED   1
#define BLUE -1
#define PLAYER_RED   2
#define PLAYER_BLUE -2
#define CUI 0
#define GUI 1
#define MANUAL 0
#define AUTO   1

// include
#include <bits/stdc++.h>
#include <windows.h>
#include <cassert>
using namespace std;

// define
typedef unsigned int uint;
#define int long long
#define repi(i,m,n) for(int i = m;i < n;i++)
#define drep(i,n,m) for(int i = n;i >= m;i--)
#define rep(i,n) repi(i,0,n)
#define rrep(i,n) repi(i,1,n+1)
#define fi first
#define se second
typedef pair<int,int> P;
typedef vector<int> vi;
const int INF = 1e18+7;
const int inf = 1e9+7;

// #include <boost/dynamic_bitset.hpp> // サイズを動的に変更するため
// typedef boost::dynamic_bitset<> Bit;
// srand((unsigned int)time(NULL));

#endif