from data import data_processing
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import json
from flask import request
import pickle
import os

class Prediction_Models():

    model_name_mapping = {
    'rf': type(RandomForestClassifier()).__name__,
    'dt': type(DecisionTreeClassifier()).__name__
    }

    def __init__(self, model_name, **params):
        if model_name == 'rf':
            self.model_name = Prediction_Models.model_name_mapping['rf']
            self.model_func = RandomForestClassifier()
        elif model_name == 'dt':
            self.model_name = Prediction_Models.model_name_mapping['dt']
            self.model_func =  DecisionTreeClassifier()
        else:
            raise Exception('Is not a valid model selection')
        self.params = params
        self.picklefile_name = f'{self.model_name}.pkl'
        self.version = 0
        self.accuracy_score = 0
        self.feature_importance = []



    #load the machine learning model functions when given the model name and
    # here we assume the user wants to see the latest version of model function
    @classmethod
    def load_model_by_name(cls,model_name):
        file_name = f'{cls.model_name_mapping[model_name]}.pkl'
        #check if the model (pickle file) has been built
        if not os.path.isfile(file_name):
            return None
        try:
            f = open(file_name,'rb')
            row = pickle.load(f)
        except:
            raise Exception('problem occured when opening the pickle file')
        #looping over the model objects in pickle file and only return the last one
        while row:
            try:
                row = pickle.load(f)
            except:
                break
        model = row
        f.close()
        return model


    @classmethod
    def load_model_by_version(cls,model_name,version):
        file_name = f'{cls.model_name_mapping[model_name]}.pkl'
        #check if the model (pickle file) has been built
        if not os.path.isfile(file_name):
            return None
        try:
            f = open(file_name,'rb')
            row = pickle.load(f)
        except:
            raise Exception('problem occured when opening the pickle file')

        while row:
            if row.version == v:
                f.close()
                return row
            c = pickle.load(f)
        return None


    def json(self):
        return {'model_name': self.model_name, 'model_function': str(self.model_func), 'model_params': str(self.params), 'model_version': self.version,\
         'accuracy_score': self.accuracy_score, 'feature_importance': str(self.feature_importance)}

    #train ML models given the parameters (retraining model)
    def train_model(self, **kwargs):
        #pass in the training/testing datasets
        #this needs to pass in everytime bc the training data might change
        data_dict = data_processing()
        X_train = data_dict['X_train']
        y_train = data_dict['y_train']
        X_test = data_dict['X_test']
        y_test = data_dict['y_test']
        #build model based on the given model name by user
        model = self.model_func
        model.set_params(**kwargs)
        model.fit(X_train,y_train)
        y_pred = model.predict(X_test)
        self.params = kwargs
        self.accuracy_score = accuracy_score(y_test, y_pred)
        self.feature_importance = model.feature_importances_
        self.version += 1
        self.model_func = model
        #create pickledump objectives which incude the model and the current accuracy_score for this model
        try:
            pickle.dump(self, open(self.picklefile_name,'ab'))
        except:
            raise Exception(f'Problem occured when writing to {self.picklefile_name}')
