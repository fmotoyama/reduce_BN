# reduce_BN
ブーリアンネットワーク（Boolean Network,BN）を、BDD（Binary Decision Diagram）のApply演算を用いて低次元化します。低次元化では、固定アトラクタの情報を保存しつつBNの次元数を小さくします。

低次元化の流れは

1. BNを生成する
2. BNのFVS（Feedback Vertex Set）を求める
3. Apply演算で低次元化計算をするために必要となる「計算順序」を、BNのインタラクショングラフとFVSから求める
4. 「計算順序」に従ってAllpy演算を行い低次元化する

となります。main.pyではこれらを行い、また必要に応じていくつかのグラフ画像を出力します。

## Usage
1. make_f.py内でBNを定義する
2. main.pyでmake_f.py内のBNを選択する
3. main.pyを実行し、そのBNを低次元化する

現在のmain.pyでは、「低次元化前後のBNのインタラクショングラフ」、「元BNのもつ論理関数のうちの1つを表すBDD」、「低次元化前後のBNの状態遷移図」をfigureフォルダに出力します。

## Requirement
graphviz 2.38

## Note
・BDDを効率的に処理するためのテクニックのいくつかを実装できていません。

・get_FVS.pyで求めるFVSは、最小FVSではありません。
