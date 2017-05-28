from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

import numpy as np
import os
from random import shuffle

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import sklearn.metrics as metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib
from sklearn import svm
from sklearn.model_selection import train_test_split

import simplejson as json
import jieba
import logging
import sys
import pickle

from sklearn.preprocessing import minmax_scale

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))
#w2v_model = Word2Vec.load('./shnu/shnu_w2v_alt.bin').wv
w2v_model = KeyedVectors.load_word2vec_format('./juice.bin',unicode_errors='ignore',binary=True)
jieba.enable_parallel(4)

dest = "./shnu/"
files = os.listdir(dest)
sources = {}
file_map= {}
count=0
x_train_pos = []

x_train_neg = []
x_test = []

train=[]

pos=['classification_pos']

neg=['classification_neg']

all = len(pos)
for name in pos:

    f = open(dest+name+'.json',errors='ignore')
    train_docs = json.load(f)
    for train_doc in train_docs:
        words = jieba.cut(train_doc['text'])
        vector = np.zeros(300)
        word_num = 0
        words = list(words)
        all = len(words)
        count = 0
        for word in list(words):
            count += 1
            print(count, ' / ', all)
            if word in w2v_model:
                vector += w2v_model[word]
                word_num += 1
        if word_num > 0:
            vector = vector / word_num
        x_train_pos.append(vector)

print('pos vector extracted')


all = len(neg)
for name in neg:

    f = open(dest+name+'.json',errors='ignore')
    train_docs = json.load(f)
    for train_doc in train_docs:
        words = jieba.cut(train_doc['text'])
        vector = np.zeros(300)
        word_num = 0
        words = list(words)
        all = len(words)
        count = 0
        for word in list(words):
            count += 1
            print(count, ' / ', all)
            if word in w2v_model:
                vector += w2v_model[word]
                word_num += 1
        if word_num > 0:
            vector = vector / word_num
        x_train_neg.append(vector)

print('neg vector extracted')

x_train=[]
x_train.extend(x_train_pos)
x_train.extend(x_train_neg)
y_train=[1]*len(x_train_pos)+[0]*len(x_train_neg)


m=joblib.load('./shnu/shnu_w2v_svc_linear.m')
print('w2v svm linear')
preds = m.predict(x_train)
print(metrics.classification_report(y_train, preds))
print(metrics.confusion_matrix(y_train, preds))

m=joblib.load('./shnu/shnu_w2v_svc_rbf.m')
print('w2v svm rbf')
preds = m.predict(x_train)
print(metrics.classification_report(y_train, preds))
print(metrics.confusion_matrix(y_train, preds))

m=joblib.load('./shnu/shnu_w2v_nb_b.m')
print('w2v BernoulliNB')
preds = m.predict(x_train)
print(metrics.classification_report(y_train, preds))
print(metrics.confusion_matrix(y_train, preds))

m=joblib.load('./shnu/shnu_w2v_nb_g.m')
print('w2v GaussianNB')
preds = m.predict(x_train)
print(metrics.classification_report(y_train, preds))
print(metrics.confusion_matrix(y_train, preds))

m=joblib.load('./shnu/shnu_w2v_nb_m.m')
print('w2v MultinomialNB')
preds = m.predict(minmax_scale(x_train))
print(metrics.classification_report(y_train, preds))
print(metrics.confusion_matrix(y_train, preds))

