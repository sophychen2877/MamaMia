import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from mlxtend.plotting import plot_decision_regions
from sklearn.metrics import classification_report
import time
import re

from textblob import TextBlob

tweets = pd.read_csv('tweets.csv')



def count_word(x,posneg):
    count=0
    for i in re.findall(r'[\w]+',x):
        if i.lower() in posneg:
            count+=1
    return count


def get_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return 'positive'
    elif sentiment < 0:
        return 'negative'
    else:
        return 'neutral'

pos_words = pd.read_csv('positive-words.txt', skiprows=35, names=['words'])
pos_words = pos_words['words'].values.tolist()
neg_words = pd.read_csv('negative-words.txt', skiprows=35, names=['words'])
neg_words = neg_words['words'].values.tolist()

'''
Data Processing 
- apply textblob to retrieve labal (sentiment for each tweet)
- convert string variables to useable, potentially meaning 

'''
tweets['sentiment'] = tweets['text'].apply(get_sentiment)
tweets['sentiment_convert']=tweets['sentiment'].map({'neutral':0,'negative':-1,'positive':1})

tweets['created_at']=pd.to_datetime(tweets['created_at'], format='%Y-%m-%d %H:%M:%S')
tweets['hour']=tweets['created_at'].apply(lambda x:x.hour)
tweets['dayofweek']=tweets['created_at'].apply(lambda x:x.dayofweek)
tweets['num_chars']=tweets['text'].str.len()
tweets['num_words']=tweets['text'].apply(lambda x: len(x.split(' ')))
tweets['num_ats']=tweets['text'].str.count('@')
tweets['countofRT']=tweets['text'].str.count('RT')

tweets['countofpostv']=tweets['text'].apply(lambda x: count_word(x,pos_words))
tweets['positiveratio']=tweets['countofpostv']/tweets['num_words']
tweets['countofnegtv']=tweets['text'].apply(lambda x: count_word(x,neg_words))
tweets['negativeratio']=tweets['countofnegtv']/tweets['num_words']


'''
Build MachineLearningModels

'''
#obtain features and assign to X
X=pd.get_dummies(tweets[['hour','dayofweek']]).\
assign(num_chars=tweets['num_chars']).\
assign(num_words=tweets['num_words']).\
assign(num_ats=tweets['num_ats']).\
assign(countofpostv=tweets['countofpostv']).\
assign(countofnegtv=tweets['countofnegtv']).\
assign(positiveratio=tweets['positiveratio']).\
assign(negativeratio=tweets['negativeratio'])

#assign label to y
y=tweets['sentiment_convert']

#train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

#apply model 1) -randomforestclassifier with hyperparameter of 75
rf = RandomForestClassifier(n_estimators=75)
cross_score_rf = cross_val_score(rf,X_train,y_train,cv=5).mean()
#apply model 2)decisiontreeclassifier with max_depth =5
clf=DecisionTreeClassifier(max_depth=5)
cross_score_clf = cross_val_score(clf,X_train,y_train,cv=5).mean()
#apply model 3) KNN with neighbor of 15
knn = KNeighborsClassifier(n_neighbors=15)
cross_score_knn = cross_val_score(knn,X_train,y_train,cv=5).mean()
#apply model 4) svc with kernel function 'rbf'
svc=SVC(kernel='rbf')
cross_score_svc = cross_val_score(svc,X_train,y_train,cv=5).mean()
#apply model 5) logisticregression with kernel function 'rbf'
lr=LogisticRegression(penalty='l1',C=0.01)

model=rf.fit(X_train, y_train)
y_pred=model.predict(X_test)
rf.score(X_test, y_test)