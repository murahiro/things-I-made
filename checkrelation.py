#coding: UTF-8
from requests_oauthlib import OAuth1Session
import json
import sys
import networkx as nx
import pickle
import matplotlib.pyplot as plt
import time

#自分の周りのユーザ100人のフォロー関係を調べ、有効グラフを作成するプログラム

global c
c = 0

def checkrelation(x,y):　#ユーザｘとｙのフォロー関係を調べエッジを追加する関数
	params = {'source_id':x,'target_id':y}
	req = twitter.get("https://api.twitter.com/1.1/friendships/show.json", params = params)
	result = json.loads(req.text)
	try:
		if result["relationship"]["target"]["following"] == True:
			g.add_edge(y,x)
		if result["relationship"]["source"]["following"] == True:
			g.add_edge(x,y)
	except:
		pass

g = nx.DiGraph()

with open('cluster100.txt','rb') as f:
	cluster0 = pickle.load(f)

cluster = []

for cl in cluster0:
	cluster.append(cl)

CK = 
CS = 
AT = 
AS =    # Accesss Token Secert

twitter = OAuth1Session(CK,CS,AT,AS)

i = 0

checkrelation(1141728799,2341595714)



nx.draw(g)
plt.show()

with open('cluster100granew.txt','wb') as f:
	pickle.dump(g,f)