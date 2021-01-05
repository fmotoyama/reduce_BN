# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 13:07:27 2020

@author: f.motoyama
"""

import numpy as np
from graphviz import Digraph
import itertools 
from copy import copy

'''
def wiring_diagram(f_dict):     
    """f_dictのwiring diagramを描画する"""
    G = Digraph(format='png',engine='sfdp')#fdp neato
    G.attr('node', shape='circle', fontsize='20', width='0.75')
    #G.attr('graph',splines='curved')

    for n in f_dict:
        if f_dict[n] != [] and type(f_dict[n]) is not int:
            V = itertools.chain.from_iterable(f_dict[n])
            V = set([abs(v) for v in V])
            for v in V:    
                G.edge(str(v),str(n))
    #print(G)
    G.render('./figure/wiring_diagram')
'''  
def wiring_diagram(parent,fname='wiring_diagram'):
    """parent(dict型)のインタラクショングラフを描画する"""
    G = Digraph(format='png', engine='sfdp')#neato
    #fontsize = 14, width=0.75
    G.attr('node', shape='circle')
    G.attr('graph', splines = 'curved', overlap = '0:')#scalexy
    G.attr('edge', arrowsize = '0.5', color="#00000080")
    
    for key in parent:
        for p in parent[key]:
            G.edge(str(p),str(key))
    #図を保存
    G.render('./figure/{}'.format(fname))



def binary_tree(bdd,fname='binary_tree'):
    """dictからBDDを描画する"""    
    V={}       #各変数の所属しているノード番地を変数ごとに格納
    G = Digraph(format='png')
    G.attr('node', shape='circle', fixedsize='true', width='0.75', fontsize='20')
    G.attr('edge', fontsize='20')
    
    if type(bdd) is int:
        #BDDが定数のとき
        G.node(str(bdd),shape='square')
        G.render('./figure/{}'.format(fname))
        return
    
    G.node(str(0),'0',shape='square'); G.node(str(1),'1',shape='square')

    for key in bdd:
        #Vごとにkeyを取得
        v = bdd[key][0]
        if v not in V:
            V[v] = []
        V[v] += [key]
    for v in V:
        #変数ごとに行を整列
        with G.subgraph() as s:
            s.attr(rank='same')
            for key in V[v]:
                s.node(str(key),str(v))     #node(値：ノードの番地(bddでのkey), ラベル：変数名)
    
    count=100       #○、|をまとめたくない場合に使う
    if type(bdd) is int:
        if bdd==0: G.node('0')
        elif bdd==1: G.node('1')
    else:
        for key in bdd:
            #"""
            G.edge(str(key),str(bdd[key][1]),label='0',arrowhead='odot')#,arrowhead='odot'
            G.edge(str(key),str(bdd[key][2]),label='1',arrowhead='dot')#,arrowhead='dot'
            """
            #○、|をまとめたくない場合に使う
            if bdd[key][1]==0:
                G.node(str(count),'0',shape='square')
                G.edge(str(key),str(count),label='0',arrowhead='odot')
                count+=1
            elif bdd[key][1]==1:
                G.node(str(count),'1',shape='square')
                G.edge(str(key),str(count),label='0',arrowhead='odot')
                count+=1
            else:
                G.edge(str(key),str(bdd[key][1]),label='0',arrowhead='odot')
            if bdd[key][2]==0:
                G.node(str(count),'0',shape='square')
                G.edge(str(key),str(count),label='1',arrowhead='dot')
                count+=1
            elif bdd[key][2]==1:
                G.node(str(count),'1',shape='square')
                G.edge(str(key),str(count),label='1',arrowhead='dot')
                count+=1
            else:
                G.edge(str(key),str(bdd[key][2]),label='1',arrowhead='dot')
            #"""
                
    #print(G)
    #G.render('./figure/binary_tree')
    G.render('./figure/{}'.format(fname))

"""
#変数での整列のテスト
a={}
a[10]=[0,11,13]
a[11]=[1,0,12]
a[12]=[2,0,14]
a[13]=[2,0,1]
a[14]=[3,0,1]
draw(a)
"""

def transition_diagram(TT,fname='transition_diagram'): 
    """真理値表TT(2,2^n,n)を入力として、状態遷移図を描画する"""
    temp = TT.shape
    l = temp[1]     #状態の個数
    n = temp[2]     #変数の個数
    
    if n <= 4:
        #変数が4つ以下のとき、2進数を表示
        ttl = np.empty(l,dtype = f'<U{n}')
        ttr = np.empty(l,dtype = f'<U{n}')
        for i in range(l):
            char_l = np.where(TT[0][i],'1','0')
            char_r = np.where(TT[1][i],'1','0')
            str_l = str()
            str_r = str()
            for j in range(n):
                str_l += char_l[j]
                str_r += char_r[j]
            ttl[i] = str_l
            ttr[i] = str_r
    else:
        #変数が5つ以上のとき、10進数に変換したものを表示
        digit = len(str(l-1))
        ttl = np.empty(l,dtype = f'<U{digit}')
        ttr = np.empty(l,dtype = f'<U{digit}')
        for i in range(l):
            True_id_l = np.where(TT[0][i])
            True_id_r = np.where(TT[1][i])
            int_l = 0; int_r = 0
            for index in True_id_l[0]:
                int_l += 2**index
            for index in True_id_r[0]:
                int_r += 2**index
            ttl[i] = str(int_l)
            ttr[i] = str(int_r)        
        
    
    G = Digraph(format='png',engine='twopi')#dot
    #G.attr(rankdir='TB') #'TB'
    G.attr('node', fixedsize='true', width='0.75', fontsize='20')
    for i in range(l):
        if ttl[i] == ttr[i]:
            #G.attr('node',shape='doublecircle')    #二重丸にならないことがあるので下の文に改良
            G.node(ttl[i],shape='doublecircle',color='red')
            G.edge(ttl[i],ttr[i])
        else:
            G.attr('node',shape='circle')
            G.edge(ttl[i],ttr[i])
           
    #print(G)
    G.render('./figure/{}'.format(fname))   


def transition_diagram2(F,FF): 
    """PBNについて、真理値表の左側F、右側FF、遷移確率を入力として、状態遷移図を描画する"""
    l=len(F)        #状態の個数
    n=len(F[0])     #変数の個数
    f=[]; ff=[]     #F,FFのstr版
    for i in range(l):      #前状態
        temp=''
        for j in range(n):
            temp+=str(F[i][j])
        f+=[temp]
        ff+=[[]]
        for k in range(len(FF[i])):     #後状態
            ttemp=''
            for j in range(n):
                ttemp+=str(FF[i][k][j])
            ff[i]+=[[ttemp,str(FF[i][k][-1])]]

    G = Digraph(format='png',engine='dot')
    #G.attr(rankdir='TB') #'TB'
    G.attr('node', fontsize='20')
    for n in range(l):
        for nn in range(len(ff[n])):
            '''
            #固定点を強調
            if f[n]==ff[n][nn][0]:
                G.node(str(f[n]),shape='doublecircle',color='red')
                G.edge(str(f[n]),str(ff[n][nn][0]),label=ff[n][nn][1])
            else:
                G.attr('node',shape='circle')
                G.edge(str(f[n]),str(ff[n][nn][0]),label=ff[n][nn][1])
            '''
            G.attr('node',shape='circle')
            G.edge(str(f[n]),str(ff[n][nn][0]),label=ff[n][nn][1])
           
    #G.node('x1x2x3',shape='circle', fontsize='13', fontname='times-itaric')
    #print(G)
    G.render('./figure/transition_diagram')



def order_tree(h_order, vroot, fvs):
    """vrootに代入操作を行う計算順序を表す木構造を描画"""
    G = Digraph(format='png')
    G.attr('graph', rankdir='LR', constraint='false')#, ordering="out"
    G.attr('node', shape='circle', fixedsize='true', width='0.75', fontsize='20',style='filled',fillcolor='white')
    G.attr('edge', style = "dashed", penwidth='1')
    
    G.node('root',str(vroot),fillcolor='#efe4b0')
    
    #ノード名（index）の決め方　→　根：root,　fvs：count,　その他：変数名そのまま
    count = -1
    def scan(v,index):
        """vを、親ノードv2と接続する"""
        nonlocal count
        
        for vp in h_order[v][0]:
            if vp in fvs:
                G.node(str(count),str(vp),fillcolor='#efe4b0')
                G.edge(str(count),str(index))
                count -= 1
            else:
                G.edge(str(vp),str(index), style = "solid", penwidth='2')
                scan(vp,str(vp))
        
        for vp2 in h_order[v][1]:
            G.edge(str(vp2),str(index))
    
    scan(vroot,'root')    
    G.render('./figure/order_tree')
    


def order_tree2(h_order, vroot, fvs):
    """色付きorder_tree"""
    c = color()
    
    G = Digraph(format='png')
    G.attr('graph', rankdir='LR', constraint='false', ranksep='0.3')
    G.attr('node', shape='circle', fixedsize='true', width='0.75', fontsize='20',style='filled',fillcolor='white')
    G.attr('edge', style = "dashed", penwidth='1')
    
    G.node('root',str(vroot),fillcolor='#efe4b0')
    
    #ノード名（index）の決め方　→　根：root,　fvs：count,　その他：変数名そのまま
    count = -1
    pathcolor = c.rgbhex
    def scan(v,index):
        """vを、親ノードv2と接続する"""
        nonlocal count, pathcolor
        
        path = True    #分岐でないことを判定
        for vp in h_order[v][0]:
            if vp in fvs:
                G.node(str(count),str(vp),fillcolor='#eeeeee',shape='doublecircle')
                G.edge(str(count),str(index))
                count -= 1
            else:
                if path == False:
                    pathcolor = c.hue()
                path = False
                G.node(str(vp),fillcolor=pathcolor)
                G.edge(str(vp),str(index), style = "solid", penwidth='2')
                scan(vp,str(vp))
        
        for vp2 in h_order[v][1]:
            G.edge(str(vp2),str(index))
    
    scan(vroot,'root')    
    G.render('./figure/order_tree')



class color:
    def __init__(self):
        self.rgb = np.array([160,240,100])
        self.rgbhex = self.dec2hex(self.rgb)
        self.rgbmax = np.max(self.rgb)
        self.rgbmin = np.min(self.rgb)
        self.pos = 3 - np.argmax(self.rgb) - np.argmin(self.rgb)      #pos%3がargとなる
        self.sign = 1                       #符号
        self.step = 50
        
    def dec2hex(self, rgb):
        rgb = rgb.astype(np.int64)
        return '#' + hex(rgb[0])[2:].zfill(2) + hex(rgb[1])[2:].zfill(2) + hex(rgb[2])[2:].zfill(2)
    
    def hue(self):
        """彩度を1step進め、rgbを返す"""
        self.rgb[self.pos%3] += self.step * self.sign
        while self.rgb[self.pos%3] < self.rgbmin or self.rgbmax < self.rgb[self.pos%3]:
            #超過分（絶対値）
            op = min(abs(self.rgb[self.pos%3]-self.rgbmax),abs(self.rgb[self.pos%3]-self.rgbmin))
            #超過部分を修正
            self.sign *= -1
            self.rgb[self.pos%3] += op * self.sign
            #次の位置に分配
            self.pos += 1
            self.rgb[self.pos%3] += op * self.sign
        return self.dec2hex(self.rgb)
            
        
        


















