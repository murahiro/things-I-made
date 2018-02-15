# coding: utf-8
from requests_oauthlib import OAuth1Session
import json
import sys
import networkx as nx
import pickle
import matplotlib.pyplot as plt

#checkrelationで取得したグラフに対してページランクを適用

with open('cluster100gra.txt','rb') as f:
	g = pickle.load(f)

pr=nx.pagerank(g,alpha=0.85)

pagerank100 = {}

for k, v in sorted(pr.items(), key=lambda x:x[1]):
    print(k, v)
    pagerank100[k] = v

with open('100pr.txt','wb') as f:
	pickle.dump(pagerank100,f)

