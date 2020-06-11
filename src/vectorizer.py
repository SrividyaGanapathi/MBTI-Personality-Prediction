"""
This module contains functions to vectorize the list of preprocessed posts using the Count Vectorizer.
"""
import os
import yaml
import numpy as np
import logging
logger = logging.getLogger()
from sklearn.feature_extraction.text import CountVectorizer
import pickle

with open(os.path.join("config", "config.yml"), "r") as f:
    config = yaml.safe_load(f)



logger.debug('Running the vectorizer functions')


def vectorize(config,list_posts):
    '''Vectorizes the preprocessed data using Count Vectorizer

        Args:
            config: Config dictionary
            list_posts: List of all preprocessed posts (data/list_posts.npy)

        Returns:
            X_cnt: Vectorized form of all inputs, i.e. now # of words = # of features
        '''

    if all(isinstance(item, str) for item in list_posts):
        cntizer = CountVectorizer(analyzer="word",
                                     max_features=config['vec']['max_features'],        # Posts to a matrix of token counts
                                     tokenizer=None,
                                     preprocessor=None,
                                     stop_words=None,
                                     max_df=config['vec']['max_df'],
                                     min_df=config['vec']['min_df'])

        # Learn the vocabulary dictionary and return term matrix
        X_cnt = cntizer.fit_transform(list_posts).toarray()

        pickle.dump(cntizer, open(config['vec']['cntizer'], "wb"))

        np.save(config['vec']['train_vec'], X_cnt)
        return X_cnt
    else:
        return

def vec(args):
    '''Runs the vectorizer function that saves the term matrix and the vectorizer for future applications

    Args:
        None

    Returns:
        None
    '''
    logger.debug('Running the vectorizer function')
    list_posts = np.load(config['preprocess']['list_posts'])
    try:
        vectorize(config,list_posts)

    except Exception as e:
        logger.error(e)
        return
