"""
This module contains functions to split the data in train and test subsets, fit the XGBoost model to the train data,
test the model and calculate accuracy as the evaluation metric.
"""
import os
import yaml

import logging
logger = logging.getLogger()
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import pickle

with open(os.path.join("config", "config.yml"), "r") as f:
    config = yaml.safe_load(f)

X = np.load(config['model']['X_path'])

def xgb(config,X):
    """ Function to fit 4 xgb models, one for each type-indicator
    Args:
            config: Config dictionary
            X: Vectorized form of all inputs

        Returns:
            accuracy_list: List of accuracies of the 4 models.

    """
    if isinstance(X,np.ndarray):
        type_indicators = list(config['model']['type_indicators'])

        accuracy_list=[]
        Y_1 = np.load(config['model']['Y_path'])

        # Let's train type indicator individually
        for l in range(len(type_indicators)):
            logger.info("%s ..." % (type_indicators[l]))

            Y = Y_1[:, l]

            # split data into train and test sets
            seed = config['Train_test']['seed']
            test_size = config['Train_test']['test_size']
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

            # fit model on training data
            logger.debug('Fitting the XGB model')
            model = XGBClassifier(**config['model']['params'])
            model.fit(X_train, y_train)


            filename = "data/models/"+str(l+1)+'_model.pickle.dat'
            pickle.dump(model, open(filename, 'wb'))
            # make predictions for test data
            y_pred = model.predict(X_test)
            predictions = [round(value) for value in y_pred]
            # evaluate predictions
            accuracy = accuracy_score(y_test, predictions)
            logger.info(confusion_matrix(y_test, predictions))
            with open(config['model']['results'], 'a') as results:
                results.write("Confusion matrix: " + str(confusion_matrix(y_test, predictions)) + "\n")
                results.write( "Accuracy: "+type_indicators[l] + str(accuracy) + "\n")
            accuracy_list.append(accuracy)

        return accuracy_list
    else:
        return



def xgb_model(args):
    '''Fetches the data from the raw source and dumps it at the location specified

    Args:
        None

    Returns:
        None
    '''
    logger.debug('Running the xgb function')
    try:
        xgb(config,X)

    except Exception as e:
        logger.error(e)
        return