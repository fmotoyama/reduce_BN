# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 23:00:06 2020

@author: motoyama
"""
from graphviz import Digraph
import numpy as np
import random
from copy import copy

def make_sf(n,b):
    """"
    p = 1/x^b
    bを大きくすると疎になる
    n:ノード数
    """
    #ノード番号の集合
    node = range(0,n)
    #各ノードの親ノードを記録
    pnode = {}
    #各ノードの次数を記録
    dim = np.zeros(n)
    
    #確率分布
    p_list = np.empty([n+1])
    p_list[0] = 0
    for i in range(1,n+1):
        #p_list[i] ： 入り次数がi以下になる確率 次数0になる確率は0
        p_list[i] = p_list[i-1] + 1/(i**b)
    p_sum = p_list[-1]
    
    for i in range(n):
        temp = random.random() * p_sum      #iの入り次数の確率
        for d, p in enumerate(p_list):
            if temp < p:
                #dは0~nの整数値をとる
                dim[i] = d
                pnode[i] = random.sample(node, d)     #nodeからj個を重複なく選ぶ
                break
    return pnode
    

def network_to_f(pnode):
    """pnodeから、AND（OR）で構成されるfを生成する"""
    f_dict = {}
    for key in pnode:
        f_dict[key] = [pnode[key]]                  #AND
        #f_dict[key] = [[j] for j in pnode[key]]     #OR
    
    return f_dict




"""
import drawset
pnode = make_sf(50,1.5)
drawset.wiring_diagram(pnode)
f_dict = network_to_f(pnode)
"""









