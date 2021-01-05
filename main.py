# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 12:26:55 2019

@author: motoyama
"""

import BooleanNetwork
import stopwatch
from make_f import make_f
import drawset


time = stopwatch.stopwatch()

#ネットワーク（BN）を生成　fvsが与えられていないときは次のBインスタンスで得る。
f_dict, fvs = make_f('1')      #make_f.pyにあるネットワークを選択
time.rap("ネットワーク生成")

#Bインスタンスを作成して、BNをBDDの集合として扱う　（+　fvsを求める）
B = BooleanNetwork.BN(f_dict, fvs)
time.rap("BNのBDD生成")

#BNを低次元化 
B.SimplifyBN2()         #低次元化の際にインタラクショングラフ上でたどった道のりをorder_tree.pngとして描画
#B.SimplifyBN()          #ふつうに低次元化
time.rap("低次元化")


#BNのインタラクショングラフを描画
drawset.wiring_diagram(B.parent,"BN")
#低次元化後BNのインタラクショングラフを描画
r_parent = B.BN_to_parent(B.r_BN)
drawset.wiring_diagram(r_parent,"r_BN")

#BNの1つの変数のBDDを描画
bdd = B.GetBDD(B.BN[next(iter(B.r_BN))])
drawset.binary_tree(bdd)

#低次元化前後のBNの真理値表と定常状態を求める（BNのサイズが大きいと実行できない）
TrueTable, SteadyState = B.MakeTrueTable(B.BN)
r_TrueTable, r_SteadyState = B.MakeTrueTable(B.r_BN)
#低次元化前後のBNの状態遷移図を描画
drawset.transition_diagram(TrueTable,'TD')
drawset.transition_diagram(r_TrueTable,'r_TD')



"""
f11 = B.BN[11]
bdd = B.GetBDD(B.BN[11])
drawset.binary_tree(bdd,11)
f11_2 = B.AssignConst(f11,[[9],[1]])
bdd2 = B.GetBDD(f11_2)
drawset.binary_tree(bdd2,'11+')
"""









