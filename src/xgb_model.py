import os
import yaml
import pandas as pd
import logging
logger = logging.getLogger()
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle





def xgb(config):
    X = np.load(config['model']['X_path'])
    type_indicators = list(config['model']['type_indicators'])
    print(type_indicators)
    param = {}

    param['n_estimators'] = 300
    param['max_depth'] = 2
    param['nthread'] = 8
    param['learning_rate'] = 0.1

    print(len(type_indicators))

    # Let's train type indicator individually
    for l in range(len(type_indicators)):
        print("%s ..." % (type_indicators[l]))

        Y = np.load(config['model']['Y_path'])

        Y = Y[:, l]


        # split data into train and test sets
        seed = 786
        test_size = 0.20
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

        # fit model on training data
        model = XGBClassifier(**param)
        model.fit(X_train, y_train)

        filename = "data/"+str(l)+'_model.sav'
        pickle.dump(model, open(filename, 'wb'))
        # make predictions for test data
        y_pred = model.predict(X_test)
        predictions = [round(value) for value in y_pred]
        # evaluate predictions
        accuracy = accuracy_score(y_test, predictions)
        print("* %s Accuracy: %.2f%%" % (type_indicators[l], accuracy * 100.0))



def xgb_model(args):
    '''Fetches the data from the raw source and dumps it at the location specified

    Args:
        None

    Returns:
        None
    '''
    logger.debug('Running the xgb function')
    try:

        with open(os.path.join("config", "config.yml"), "r") as f:
            config = yaml.safe_load(f)

        xgb(config)
        print("XGB applied successfully")

    except Exception as e:
        logger.error(e)
        print(e)
        return