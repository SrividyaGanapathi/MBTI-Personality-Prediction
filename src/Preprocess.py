"""
This module contains functions to preprocess the raw data by removing stopwords, punctuations and lemmatization.
"""
import os
import yaml
import json
from nltk.stem import PorterStemmer, WordNetLemmatizer
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk import word_tokenize
import logging
import numpy as np
logger = logging.getLogger()
import re
import pandas as pd

with open(os.path.join("config", "config.yml"), "r") as f:
    config = yaml.safe_load(f)



logger.debug('Running the preprocess functions')

    ####Binarize Type Indicator####
def translate_personality(personality,config):
    # transform mbti to binary vector
    bin_Pers_dict = json.loads(config['preprocess']['b_Pers'])
    return [bin_Pers_dict[l] for l in personality]


def translate_back(personality,config):
    # transform binary vector to mbti personality
    bin_Pers_list = list(config['preprocess']['b_Pers_list'])
    s = ""
    for i, l in enumerate(personality):
        s += bin_Pers_list[i][l]
    return s




def x_ylists(config,df):
    ''' Preprocesses the data by removing punctuations, stopwords and MBTI profiles from the posts
    Args:
        config: Config dictionary
        df: Raw data taken from s3 and stored in data/raw

    Returns:
        list_posts: List of all posts (numpy array)
        list_personality: List of all personalities (numpy array)

    '''

    if all(isinstance(item, str) for item in df.posts):


        remove_stop_words = config['preprocess']['remove_stop_words']
        remove_mbti_profiles = config['preprocess']['remove_mbti_profiles']
        type_list=list(config['preprocess']['unique_type_list'])
        type_list = [x.lower() for x in type_list]
        stemmer = PorterStemmer()
        lemmatiser = WordNetLemmatizer()
        cachedStopWords = stopwords.words("english")

        list_personality = []
        list_posts = []
        len_data = len(df)
        i = 0

        for row in df.iterrows():
            i += 1
            if (i % 1000 == 0 or i == 1 or i == len_data):
                logger.info("%s of %s rows" % (i, len_data))

                ##### Remove and clean comments
            posts = row[1].posts
            temp = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', posts)
            temp = re.sub("[^a-zA-Z]", " ", temp)
            temp = re.sub(' +', ' ', temp).lower()
            if remove_stop_words:
                temp = " ".join([lemmatiser.lemmatize(w) for w in temp.split(' ') if w not in cachedStopWords])
            else:
                temp = " ".join([lemmatiser.lemmatize(w) for w in temp.split(' ')])

            if remove_mbti_profiles:
                for t in type_list:
                    temp = temp.replace(t, "")

            type_labelized = translate_personality(row[1].type,config)
            list_personality.append(type_labelized)
            list_posts.append(temp)

        list_posts = np.array(list_posts)
        list_personality = np.array(list_personality)
        np.save(config['preprocess']['list_posts'], list_posts)
        np.save(config['preprocess']['list_personality'], list_personality)
        return list_posts, list_personality
    else:
        return




def preprocess(args):
    '''Creates lists of posts and personalities separately

    Args:
        None

    Returns:
        None
    '''
    logger.debug('Running the preprocess function')
    df=pd.read_csv(config['preprocess']['path'])
    try:

        x_ylists(config,df)

    except Exception as e:
        logger.error(e)
        return
