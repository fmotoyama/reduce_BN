# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 17:25:53 2020

@author: motoyama
"""

from copy import copy

class BDD:
    def __init__(self):
        self.table = {}
        #self.table[0] = '⊥'; self.table[1] = '⊤'
                    
    
    def GetNode(self,v,P0,P1):
        """(変数名,0枝番地,1枝番地)を持つノードのキー(番地)を返す"""
        if P0==P1:
            #削除規則
            return(P0)
        info = [v,P0,P1]
        for key in self.table:
            if self.table[key] == info:
                #共有規則
                return key
        ID = id(info)
        self.table[ID] = info
        return ID;       
    
    
    def GetBDD(self,f):
        """ノードfから始まるBDDを返す"""
        if f in [0,1]:
            return f
        result = {}
        def scan(n):
            if n in [0,1]:
                return n
            result[n] = copy(self.table[n])
            scan(self.table[n][1])
            scan(self.table[n][2])
        
        scan(f)
        return result
    
    
    def AP(self,op,f,g):
    
        def OR(f,g):
            """テーブルF,Gの根節点の番地を用いて論理和テーブルresultを返す"""
            #再帰で掘り進む必要がないケース
            if f==0 or f==g: return(g)  #(0,*)
            if g==0: return(f)          #(*,0)
            if f==1: return(1)          #(1,*)
            if g==1: return(1)          #(*,1)
            #再帰でシャノン展開
            #GetNode(変数名,0枝番地,1枝番地), OR(Ftopkey,Gtopkey)
            if self.table[f][0]<self.table[g][0]:
                R=self.GetNode(self.table[f][0],OR(self.table[f][1],g),OR(self.table[f][2],g))
            elif self.table[f][0]>self.table[g][0]:
                R=self.GetNode(self.table[g][0],OR(f,self.table[g][1]),OR(f,self.table[g][2]))
            elif self.table[f][0]==self.table[g][0]:         
                R=self.GetNode(self.table[f][0],OR(self.table[f][1],self.table[g][1]),OR(self.table[f][2],self.table[g][2]))
            return(R)
    
        def AND(f,g):
            """テーブルF,Gの根節点の番地を用いて論理積テーブルresultを返す"""
            #再帰で掘り進む必要がないケース
            if f==0: return(0)          #(0,*)
            if g==0: return(0)          #(*,0)
            if f==1 or f==g: return(g)  #(1,*)
            if g==1: return(f)          #(*,1)
            #再帰でシャノン展開
            if self.table[f][0]<self.table[g][0]:
                R=self.GetNode(self.table[f][0],AND(self.table[f][1],g),AND(self.table[f][2],g))
            elif self.table[f][0]>self.table[g][0]:
                R=self.GetNode(self.table[g][0],AND(f,self.table[g][1]),AND(f,self.table[g][2]))
            elif self.table[f][0]==self.table[g][0]:         
                R=self.GetNode(self.table[f][0],AND(self.table[f][1],self.table[g][1]),AND(self.table[f][2],self.table[g][2]))
            return(R)
            
        #----------AP()の処理----------
        if op==0: result=OR(f,g)
        elif op==1: result=AND(f,g)
        
        return(result)
    
            
    def NOT(self,f):
        if f == 0: return(1)
        if f == 1: return(0)
        def Not(n):
            if n==0: return(1)
            if n==1: return(0)              
            R=self.GetNode(self.table[n][0],Not(self.table[n][1]),Not(self.table[n][2]))
            return(R)
        result = Not(f)
        return(result)
            
    ####################
        
    
    def AssignConst(self,f,clist):  #clist=[[v1,v2,...],[0,1,...]]
        """グラフfの各変数に定数を代入した結果のグラフの根(または定数)を返す"""
        if f in [0,1]:
            #BDDになっておらず定数のとき
            return f
        
        bdd = self.GetBDD(f)
        #bddにclistを適用する
        for key in bdd:
            if bdd[key][0] in clist[0]:
                #key:vで分岐をしないこととする（片方の枝に素通しする）
                c = clist[1][clist[0].index(bdd[key][0])]  #定数
                bdd[key] = bdd[key][c + 1]                 #key:id
        
        def scan(n):
            """bdd[n]を調べ、枝先で再帰処理をする"""
            if n in [0,1]:
                #定数のとき
                return n
            if type(bdd[n]) is int:
                #素通ししているとき、行き先のノードを返す
                return scan(bdd[n])
            #2つの子ノードをもつとき
            R = self.GetNode(bdd[n][0], scan(bdd[n][1]), scan(bdd[n][2]))
            return R
            
        result = scan(f)
        return(result)
            



    
    

