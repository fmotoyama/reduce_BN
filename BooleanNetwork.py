# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 17:25:53 2020

@author: motoyama
"""

from copy import copy
import numpy as np
import itertools
from BDD import BDD
from get_FVS import get_FVS
import drawset


class BN(BDD):
    def __init__(self, f_dict, fvs = None):
        super().__init__()
        """
        f_dict  :BNを表す関数listのdict
        BN      :BNを表す関数BDDのdict
        Var     :変数BDDのdict
        parent  :親ノードlistのdict
        Order   :代入順序dict
        rBDD    :低次元化後BN
        f       :関数名
        n       :ノード番号
        v       :変数名
        """
        self.f_dict = f_dict
        self.l = len(f_dict); self.L = [k for k in self.f_dict.keys()]
        #Var:変数そのものを表すBDD
        self.Var = {}
        for v in self.L:
            self.Var[v] = self.GetNode(v,0,1)
        #BN:関数を表すBDD
        self.BN = {}
        for v in self.L:
            self.BN[v] = self.calc_f(v,self.Var)
        #parent:各ノードの親ノードを格納
        self.parent = {}
        for v in self.L:
            if self.f_dict[v] != []:
                if type(f_dict[v]) is int:
                    self.parent[v] = []
                else:
                    #f_dict[n]の平坦化
                    self.parent[v] = itertools.chain.from_iterable(f_dict[v])
                    #負数を正数に & 重複の削除
                    self.parent[v] = list(set([abs(v2) for v2 in self.parent[v]]))
        #fvsが与えられていないとき、求める
        if fvs == None:
            self.fvs = get_FVS(self.parent)
        else:
            self.fvs = fvs
                    
    

    def SimplifyBN(self):
        """fvs[]を用いて低次元化ネットワークを求める"""
        def GetOrder(v):
            #vの先祖を探索
            order = []                      #最終的な計算順序を格納
            def get_order(v):
                """parentをたどり、order（後順）を完成させる"""
                for v2 in self.parent[v]:
                    if v2 in self.fvs or v2 in order:
                        #v2がfvsのとき or v2に訪ねたことがあるとき（v2の親の探索が終わっているとき）
                        continue
                    #v2に初めて訪ねたので、v2の親の探索をする
                    get_order(v2)
                order.append(v)
            
            get_order(v)
            return order
    
                
        self.r_BN = {}
        self.Order = {}
        for vf in self.fvs:
            Var2 = copy(self.Var)
            
            #Getorder:探索ノードを作図 Getorder2：作図をしない軽量版
            self.Order[vf] = GetOrder(vf)
            
            #orderに従って演算
            for v in self.Order[vf]:
                Var2[v] = self.calc_f(v,Var2)
            self.r_BN[vf] = Var2[vf]
                
        return


    def SimplifyBN2(self):
        """fvs[]を用いて低次元化ネットワークを求める + orderの作成過程を描画する"""
        def GetOrder(v):
            #vの先祖を探索し、探索ノードをh_orderに記録する
            order = []          #最終的な計算順序を格納
            h_order = {}        #vを根とする半順序について、各ノードの親を格納
            def get_order(v):
                h_order[v] = [[],[]]    #[[fvs,その他],[すでにordにある]]
                """parentをたどり、order（後順）を完成させる"""
                for v2 in self.parent[v]:
                    if v2 in order:
                        h_order[v][1].append(v2)
                        continue
                    elif v2 in self.fvs:
                        h_order[v][0].append(v2)
                        continue
                    #v2に初めて訪ねたので、v2の親の探索をする
                    h_order[v][0].append(v2)
                    get_order(v2)
                order.append(v)
            
            get_order(v)
            return order, h_order
            
        self.r_BN = {}
        self.Order = {}
        l = 0
        for vf in self.fvs:
            Var2 = copy(self.Var)
            
            #orderを求める
            self.Order[vf],h_order = GetOrder(vf)
            
            #orderに従って演算
            for v in self.Order[vf]:
                Var2[v] = self.calc_f(v,Var2)
            self.r_BN[vf] = Var2[vf]
            
            #最大次数を探し、self.hub, self.orderを決定
            if l < len(self.parent[vf]):
                l = len(self.parent[vf])
                hub = vf    #fvsのうち、親が最も多いもの
                hubh_order = h_order
                
        drawset.order_tree(hubh_order, hub, self.fvs)
        return



    def MakeTrueTable(self,BN):
        """
        BNの真理値表を求める
        [[0000],[1000],...],[[1011],[0101],...] x1x2x3の順番
        """
        V = list(BN.keys()) #関数名の集合
        l = len(BN)         #ノード（関数）数
        const = []          #定数である関数 [[何桁目か,定数],...]
        non_const = []      #定数でない関数 [何桁目か,...]
        for digit,f in enumerate(BN):
            if BN[f] in [0,1]:
                const.append([digit,BN[f]])
            else:
                non_const.append(digit)
        const = np.array(const)
        ttl = np.empty((2**len(non_const),l), dtype=np.bool)    #真理値表の左側
        for c in const:
            ttl[:,c[0]] = c[1]
        ttr = ttl.copy()                                        #真理値表の右側
        SS = []             #真理値表で変化していない組
        

        #真理値表の左側を作成
        for j,digit in enumerate(non_const):
            #non_constの列について処理
            for i in range(2**len(non_const)):
                ttl[i,digit] = (i // 2**j) % 2        #左始め
        
        #真理値表の右側を作成
        for i in range(len(ttl)):
            clist = [V,ttl[i]]
            for digit in non_const:
                fx = self.AssignConst(BN[V[digit]],clist)   #fx:関数に定数を代入した値
                ttr[i][digit] = fx
            #固定点の検知
            if np.all(ttl[i] == ttr[i]):
                SS += [ttr[i]]
                
        return(np.array([ttl, ttr]), SS)
    
    
    def BN_to_parent(self,BN):
        """BNからparentを返す"""
        parent = {}
        for x,f in BN.items():
            bdd = self.GetBDD(f)
            V = []
            if type(bdd) is dict:
                #bddが定数のときVは空　dictのときbdd内のの変数を抽出
                for n in bdd:
                    V.append(bdd[n][0])
                #重複を削除
                V = list(set(V))
            
            parent[x] = V
            
        return parent
    
    

    def calc_f(self,v,F):
        """
        f_dictの表す積和形を参考に、F{}のBDDについてf[v]の演算を行う
        f_dict : dict{ノード:list[積項][変数]}, v : int
        """
        def calc_product(term):
            """"term(list)がもつ変数を全て積算したBDDを返す"""
            if len(term) == 1:
                if term[0] < 0:
                    return self.NOT(F[-term[0]])
                else:
                    return F[term[0]]
            else:
                if term[0] < 0:
                    temp = self.NOT(F[-term[0]])
                else:
                    temp = F[term[0]]
                for i in range(len(term) - 1):
                    #termにある変数をすべてOR演算で合成する
                    if term[i+1] < 0:
                        product_BDD = self.AP(1, temp, self.NOT(F[-term[i+1]]))
                    else:
                        product_BDD = self.AP(1, temp, F[term[i+1]])
                    temp = product_BDD
                return product_BDD
            
        if self.f_dict[v] == []:
            #ノードnに親がいないとき（f[v]は他から影響を受けない）
            return F[v]
        elif type(self.f_dict[v]) is int:
            #多項式でなく定数のとき（f[v]の入力が常に定数）
            return self.f_dict[v]
        elif len(self.f_dict[v]) == 1:
            #単項式のとき
            return calc_product(self.f_dict[v][0])        
        else:
            #多項式のとき
            products_BDD = []       #項ごとのBDDをlistで格納
            for term in self.f_dict[v]:
                #termごとにBDDの積を計算する
                product_BDD = calc_product(term)
                products_BDD.append(product_BDD)
            temp = products_BDD[0]
            for i in range(len(products_BDD) - 1):
                sum_BDD = self.AP(0, temp, products_BDD[i+1])
                temp = sum_BDD
            return sum_BDD

    

"""
f_dict = {
    1:[[1]],        #x1
    2:[[1,-3]],     #x1 * ^x3
    3:[[-2,4]],     #^x2 * x4
    4:[[1],[3]],    #x1 + x3
    }


B = BDD(f_dict)
F = B.BN
a = B.AP(0,F[1],F[3]) #x1 + ^x2 * x4
at = B.GetBDD(a)
#"""
    
    
    
    

