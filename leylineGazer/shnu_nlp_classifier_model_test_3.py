from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

import numpy as np
import os
from random import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import sklearn.metrics as metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB,BernoulliNB,GaussianNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

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
w2v_model_alt = Word2Vec.load('./shnu/shnu_w2v_alt.bin').wv
w2v_model = KeyedVectors.load_word2vec_format('./juice.bin',unicode_errors='ignore',binary=True)
Word2Vec.load('./shnu/shnu_w2v_alt.bin')
dest = "./shnu/classed_cut/"
files = os.listdir(dest)
sources = {}
file_map= {}
count=0
x_train_pos = []
x_train_pos_alt = []
text_train_pos = []
text_train_pos_alt = []

x_train_neg = []
x_train_neg_alt = []
text_train_neg = []
text_train_neg_alt = []

x_test = []

pos=['fb',
'shenghuan',
'xxjd',
'mathsc',
'kjc',
'bc',
'jrxy',
'xxb',
'jiangong',
'hxzx',
'res.chem']

neg=['xzx',
'renwen',
'xiejin',
'shcas',
'marx',
'iccs',
'cice',
'shkch',
'zhexue',
'jjc',
'fineart',
'xlzx',
'waiyu',
'fazheng',
'ictt',

     ]






count = 1
all = len(pos)
for name in pos:
    print(count , ' / ' , all)
    count+=1
    f = open(dest+name+'.txt',errors='ignore')
    train_docs = f.readlines()
    for train_doc in train_docs:
        words = train_doc.split()
        text_train_pos.append(words)

print('pos text extracted')


count = 1
all = len(neg)
for name in neg:
    print(count , ' / ' , all)
    count+=1
    f = open(dest + name + '.txt',errors='ignore')
    train_docs = f.readlines()
    for train_doc in train_docs:
        words = train_doc.split()
        text_train_neg.append(words)

print('neg text extracted')
train_txt = []
train_txt.extend(text_train_pos)
train_txt.extend(text_train_neg)

#with open('./shnu/shnu_train_raw.pkl','wb') as f:
#    pickle.dump(train,f)

target=[1]*len(text_train_pos)+[0]*len(text_train_neg)
train_text_x,test_text_x, train_text_y, test_text_y = train_test_split(train_txt,
                                                   target,
                                                   test_size = 0.2,
                                                   random_state = 0)

#nb


count_v0= CountVectorizer()
counts_all = count_v0.fit_transform(train_txt)
count_v1= CountVectorizer(vocabulary=count_v0.vocabulary_)
counts_train = count_v1.fit_transform(train_text_x)
count_v2= CountVectorizer(vocabulary=count_v0.vocabulary_)
counts_test = count_v2.fit_transform(test_text_x)
tfidftransformer = TfidfTransformer()
train_data = tfidftransformer.fit(counts_train).transform(counts_train)
test_data = tfidftransformer.fit(counts_test).transform(counts_test)


print('MultinomialNB')

nb_m=joblib.load('./shnu/shnu_nb_m.m')
preds=nb_m.predict(test_data)
print(metrics.classification_report(test_text_y, preds))
print(metrics.confusion_matrix(test_text_y, preds))

print('BernoulliNB')

nb_b=joblib.load('./shnu/shnu_nb_b.m')
preds=nb_b.predict(test_data)
print(metrics.classification_report(test_text_y, preds))
print(metrics.confusion_matrix(test_text_y, preds))

print('svm linear')

svclf = joblib.load('./shnu/shnu_svm_l.m')
preds = svclf.predict(test_data)
print(metrics.classification_report(test_text_y, preds))
print(metrics.confusion_matrix(test_text_y, preds))


print('svm rbf')

svmr = joblib.load('./shnu/shnu_svm_r.m')
preds = svmr.predict(test_data)
print(metrics.classification_report(test_text_y, preds))
print(metrics.confusion_matrix(test_text_y, preds))

