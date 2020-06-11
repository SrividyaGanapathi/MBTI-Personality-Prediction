"""
This module contains functions to test the functions in preprocessing, vectorizing and modelling.
"""
import warnings
warnings.filterwarnings("ignore")
import os
import yaml
import pytest

import numpy as np
import pandas as pd
import sys
from os import path

rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)

with open(os.path.join("config", "config.yml"), "r") as f:
    config = yaml.safe_load(f)

from src.Preprocess import x_ylists
from src.vectorizer import vectorize
from src.xgb_model import xgb

df = {
    'type': ['INFP','INFP','INFJ','ENTP','ENTJ'],
    'posts':["It takes a village to raise a child.", "I am quite an introvert","These people were born and raised up by the village chief", "Let's all go to the movies","Why was she baking cookies when we have to watch a movie?"]
    }

test_df = pd.DataFrame(df)

def test_preprocess_happy():
    list_posts = ['take village raise child ','quite introvert','people born raised village chief','let go movie','baking cooky watch movie ']
    list_posts_true,list_personality_true = x_ylists(config,test_df)
    assert isinstance(list_posts_true, np.ndarray)
    assert len(list_posts)==len(list_posts_true)

def test_preprocess_unhappy():
    df1 = {
        'type': ['INFP', 'INFP', 'INFJ', 'ENTP', 'ENTJ'],     # Type length has to be 4
        'posts':["It takes a village to raise a child.", True,"These people were born and raised up by the village chief", # Posts have to be strings
                 "Let's all go to the movies","Why was she baking cookies when we have to watch a movie?"]
    }
    test_df1 = pd.DataFrame(df1)
    true= x_ylists(config,test_df1)
    assert not isinstance(true, np.ndarray)

def test_vectorize_happy():
    list_posts= ['take village raise child ', 'quite introvert',
 'people born raised village chief', 'let go movie',
 'baking cooky watch movie ']
    input=np.array(list_posts)
    output = np.array([[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
       [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
       [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]])
    true = vectorize(config,input)
    assert (output==true).all()

def test_vectorize_unhappy():
    list_posts = [1,2,3,4,5]

    input=np.array(list_posts)
    true1 = vectorize(config, input)

    assert not isinstance(true1,np.ndarray)


def test_xgb_happy():
    X_cnt=np.array([[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
       [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
       [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]])



    output=[0.5, 1.0, 0.5, 0.5]
    true= xgb(config,X_cnt)
    assert (output == true)

def test_xgb_unhappy():
    list_posts_true, Y_1 = x_ylists(config, test_df)
    X_cnt = [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0],              #X_cnt has to be a np.ndarray
                      [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                      [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
                      [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]]
    true= xgb(config,X_cnt)
    assert not isinstance(true, np.ndarray)








