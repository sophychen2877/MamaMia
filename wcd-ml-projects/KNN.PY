#set the K to 3
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from collections import Counter
from math import sqrt
iris=datasets.load_iris()
X=iris.data
y=iris.target
X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=42)
y_pred=[]


#here we set the k to 3
def sort_list_smallest_3(lst):
    return [i for i,x in sorted(enumerate (lst), key = lambda x: x[1])][:3]

def euclidean_distance(a,b):
    return sqrt(sum([(i-j)**2 for (i,j) in zip(a,b)]))

distance_to_train=[[euclidean_distance(test_row_x,train_row_x) for train_row_x in X_train] for test_row_x in X_test]


for row in distance_to_train:
    sort_index = sort_list_smallest_3(row)
    y_train_value=[y_train[i] for i in sort_index]
    c=Counter(y_train_value).most_common(1)[0][0]
    y_pred.append(c)
sum([a==b for a,b in zip(y_test,y_pred)])
