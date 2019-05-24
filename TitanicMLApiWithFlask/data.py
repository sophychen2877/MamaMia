import pandas as pd
from sklearn.model_selection import train_test_split
import re

filename = 'train.csv'
def data_processing(filename):
    df = pd.read_csv(filename)

    df=df.drop(['PassengerId'],axis=1)

    #converting cabin letter to Deck, creating a new feature - deck

    deck = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "U": 8}
    #extract the cabin letter and map to deck
    df['deck'] = df['Cabin'].map(lambda x: re.compile('[a-zA-Z+]').search(x).group())
    #convert deck letter to deck number
    df['deck'] = df['deck'].map()

    df = df.drop(['cabin', 'body', 'name', 'home.dest', 'ticket', 'boat'], axis=1, errors='ignore')
    X = pd.get_dummies(df[['pclass', 'sex', 'sibsp', 'parch', 'embarked']])
    y = df['survived']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 42)
    return {'X_train': X_train,'X_test': X_test,'y_train': y_train, 'y_test': y_test}
