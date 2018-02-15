# -*- coding: utf-8 -*-
import pickle
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from sklearn import svm
import numpy as num
from sklearn.metrics import classification_report, accuracy_score
from sklearn import cross_validation
from sklearn.cross_validation import StratifiedKFold
from sklearn.utils import shuffle

#Doc2vecによって変換したニュース記事のベクトルをSVM（交差検定（ｎ＝１０）によって分類

with open("copas2500deleted.pickle","rb")as f:
	copas=pickle.load(f)

model = Doc2Vec.load("test2.model")
Svm = svm.SVC()
print(len(model.docvecs[0]))

name = num.zeros(len(copas))

henkan={"it":1,"homme":2,"movie":3,"peachy":4,"sports":5}



dim=len(model.docvecs[0])

arr = num.empty((0,float(dim)), float)



for count in range(len(copas)):
	name[count] = henkan[copas[count][0]]
	arr = num.append(arr, num.array([model.docvecs[count]]), axis=0)

name, arr = shuffle(name, arr)
accusum = 0

skf = StratifiedKFold(name, 10)
for train, test in skf:
	# print(type(test),type(train))
	print(len(arr[train]),len(name[train]))
	Svm.fit(arr[train], name[train])
	print(len(arr[test]))
	predict = Svm.predict(arr[test])
	# print ("prediction", predict)
	# print ("ground truth", name[test])
	accu = (predict == name[test]).sum() / float(predict.size)
	# print ("accuracy", accu)
	# print ("----")
	accusum += accu

print(accusum/10)

