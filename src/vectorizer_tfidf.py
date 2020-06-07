import os
import yaml
import pandas as pd
import numpy as np
import logging
logger = logging.getLogger()
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


list_posts = np.load('data/list_posts.npy')
list_personality = np.load('data/list_personality.npy')

logger.debug('Running the vectorizer functions')


def vectorize_tfidf(config,list_posts):
    # Posts to a matrix of token counts
    cntizer = CountVectorizer(analyzer="word",
                                 max_features=config['vec_tfidf']['max_features'],
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 max_df=config['vec_tfidf']['max_df'],
                                 min_df=config['vec_tfidf']['min_df'])

    # Learn the vocabulary dictionary and return term-document matrix
    print("CountVectorizer...")
    X_cnt = cntizer.fit_transform(list_posts)

    # Transform the count matrix to a normalized tf or tf-idf representation
    tfizer = TfidfTransformer()

    print("Tf-idf...")
    # Learn the idf vector (fit) and transform a count matrix to a tf-idf representation
    X_tfidf =  tfizer.fit_transform(X_cnt).toarray()
    print(type(X_tfidf))
    #feature_names = list(enumerate(cntizer.get_feature_names()))
    #open('data/vocab', 'w').write('\n'.join('%s %s' % x for x in feature_names))
    np.save('data/X_tfidf', X_tfidf)
    return

def vec_tfidf(args):
    '''Fetches the data from the raw source and dumps it at the location specified

    Args:
        None

    Returns:
        None
    '''
    logger.debug('Running the vectorizer function')
    try:

        with open(os.path.join("config", "config.yml"), "r") as f:
            config = yaml.safe_load(f)

        vectorize_tfidf(config,list_posts)
        print("X_tfidf created successfully")

    except Exception as e:
        logger.error(e)
        print(e)
        return
