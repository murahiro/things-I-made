#coding:utf-8
import math
import sys
from collections import defaultdict

#単純ベイズ分類器の実装

class NaiveBayes:
	"""Multinomial NaiveBayes"""
	def __init__(self):
		self.categories = set()     #カテゴリの集合
		self.vocabularies = set()    #ボキャブラリの集合
		self.wordcount = {}         #wordcount[cat][word] カテゴリでの単語の出現回数
		self.catcount ={}           #catcount[cat] カテゴリの出現回数
		self.denominator ={}        #denominator[cat] P(word|cat)の分母の値

	def train(self, data):
		"""ナイーブベイズ分類器の訓練"""
		#文章集合からカテゴリを抽出して辞書を初期化
		for d in data:
			cat = d[0]
			self.categories.add(cat)
		for cat in self.categories:
			self.wordcount[cat] = defaultdict(int)
			self.catcount[cat] = 0
		#文章集合からカテゴリと単語をカウント
		for d in data:
			cat, doc = d[0],d[1:]
			self.catcount[cat] += 1
			for word in doc:
				self.vocabularies.add(word)
				self.wordcount[cat][word] += 1
			#単語の条件付確率の分母の値をあらかじめ一括計算しておく（高速化のため）lenはラプラススムージング
		for cat in self.categories:
			self.denominator[cat] = sum(self.wordcount[cat].values()) + len(self.vocabularies)

	def classify(self, doc):
		"""事後確率の対数log(P(cat|doc))が最も大きなカテゴリーを返す"""
		best = None
		max = -sys.maxsize
		for cat in self.catcount.keys():
			p = self.score(doc, cat)
			if p > max:
				max = p
				best = cat
		return best


	def wordProb(self, word, cat):
		"""単語の条件付き確率 P(word|cat) を求める"""
		#ラプラススムージングを適用
		#wordcount[cat]はdefaultdict(int)なのでカテゴリに存在しなかった単語はデフォの０
		#分母はtrai()の最後で一括計算済み
		return float(self.wordcount[cat][word] + 1) / float(self.denominator[cat])

	def score(self, doc, cat):
		total = sum(self.catcount.values())
		score = math.log(float(self.catcount[cat]) / total)  # log P(cat)
		for word in doc:
			#logをとると掛け算は足し算
			score += math.log(self.wordProb(word, cat))  # log P(word|cat)
		return score

	def __str__(self):
		total = sum(self.catcount.values()) #総文章数
		return "documents: %d, vocabularies: %d, categories: %d" % (total, len(self.vocabularies), len(self.categories))

	def postProb(self, doc, cat):
		"""文書が与えられたときのカテゴリの「正規化していない（=p(doc)で割らない）」事後確率 P'(cat|doc) を求める"""
		total = sum(self.catcount.values())  # 総文書数
		pp = float(self.catcount[cat]) / total  # 事前確率P(cat)
		# 尤度 P(doc|cat) = P(word1|cat) * p(word2|cat) * ...
		# 対数をとらないので掛け算になる（非常に小さな値！）
		for word in doc:
			pp *= self.wordProb(word, cat)
		return pp

	def stopcount(self,stopcount):
		for c in self.catcount.keys():
			for k, v in self.wordcount[c].copy().items():
				if v > stopcount:
					# print(k)
					del(self.wordcount[c][k])

	def stopword(self,word):
		for words in word:
			for c in self.catcount.keys():
				try:
					del(self.wordcount[c][words])
				except KeyError:
					pass

	def showrank():
		for c in self.catcount.keys():
			rank = OrderedDict(sorted(self.wordcount[c].items(), key=lambda x:x[1]))
			for i in range(100):
				print(rank[i])



if __name__ == "__main__":
	#data(list)list[0]はカテゴリ
	data =[["yes", "Chinese", "Beijing", "Chinese"],
	["yes", "Chinese", "Chinese", "Shanghai"],
	["yes", "Chinese", "Macao"],
	["no", "Tokyo", "Japan", "Chinese"]]

	#ナイーブベイズ分類器を訓練
	nb = NaiveBayes()
	nb.train(data)
	print(nb)
	print("P(Chinese|yes) = ", nb.wordProb("Chinese", "yes"))
	print("P(Tokyo|yes) = ", nb.wordProb("Tokyo", "yes"))
	print("P(Japan|yes) = ", nb.wordProb("Japan", "yes"))
	print("P(Chinese|no) = ", nb.wordProb("Chinese", "no"))
	print("P(Tokyo|no) = ", nb.wordProb("Tokyo", "no"))
	print("P(Japan|no) = ", nb.wordProb("Japan", "no"))

	test = ["Chinese", "Chinese", "Chinese", "Chinese", "Shanghai"]
	print("log P(yes|test) =", nb.score(test, "yes"))
	print("log P(no|test) =", nb.score(test, "no"))
	print(nb.classify(test))
	p1 = nb.postProb(test, "yes")  # 正規化されていないので確率ではない！
	p2 = nb.postProb(test, "no")   # 正規化されていないので確率ではない！
	# 下のようにすると足して1になる確率になる
	print("P(yes|test) =", p1 / (p1 + p2))
	print("P(no|test)  =", p2 / (p1 + p2))