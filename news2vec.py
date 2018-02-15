# -*- coding: utf-8 -*-
import pickle
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from sys import argv

#ニュース記事をdoc2vecによってベクトル化するプログラム

with open("copas2500deleted.pickle","rb")as f:
	copas=pickle.load(f)
print(len(copas))

training_docs = []

for count in range(len(copas)):
	name = str(str(copas[count][0])+str(count))
	# print(type(name))
	# print(name)
	training_docs.append(TaggedDocument(words=copas[count][1:],tags=[name]))

dim = argv[1]


model = Doc2Vec(documents=training_docs, size=int(dim), window=8, min_count=1, dm=0)

model.save('test2.model')
# print(model.docvecs['dokujyo1'])

print(model.docvecs.most_similar('it1'))
