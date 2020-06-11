"""
This module contains all functionality of the flask app
"""
import os
from flask import render_template, request, redirect, url_for, Flask, jsonify

from flask_sqlalchemy import SQLAlchemy
import yaml
import json

from nltk.stem import PorterStemmer, WordNetLemmatizer
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords

import logging
logger = logging.getLogger()
import re
import pickle


from src.create_db import mbti_1

app = Flask(__name__, template_folder="app/templates")
app.config.from_pyfile(os.path.join('config','flaskconfig.py'))
app.static_folder = 'app/static'

# Initialize the database
db = SQLAlchemy(app)

logger.debug('Running the preprocess functions')

list_posts=[]

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

with open(os.path.join("config", "config.yml"), "r") as f:
    config = yaml.safe_load(f)

def preprocess(mytext,config):
    remove_stop_words = config['preprocess']['remove_stop_words']
    remove_mbti_profiles = config['preprocess']['remove_mbti_profiles']
    type_list=list(config['preprocess']['unique_type_list'])
    type_list = [x.lower() for x in type_list]
    stemmer = PorterStemmer()
    lemmatiser = WordNetLemmatizer()
    cachedStopWords = stopwords.words("english")

    temp = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', mytext)
    temp = re.sub("[^a-zA-Z]", " ", temp)
    temp = re.sub(' +', ' ', temp).lower()
    if remove_stop_words:
        temp = " ".join([lemmatiser.lemmatize(w) for w in temp.split(' ') if w not in cachedStopWords])
    else:
        temp = " ".join([lemmatiser.lemmatize(w) for w in temp.split(' ')])

    if remove_mbti_profiles:
        for t in type_list:
            temp = temp.replace(t, "")

    if temp!='':

        list_posts.append(temp)
        return list_posts

    else:
        return

logger.debug('Running the vectorizer functions')


def vectorize(config,my_posts):
    # Posts to a matrix of token counts
    if isinstance(my_posts, list):
        count_vec = open(config['vec']['cntizer'], 'rb')
        cntizer = pickle.load(count_vec)

        # Learn the vocabulary dictionary and return term-document matrix
        X_cnt = cntizer.transform(my_posts).toarray()

        return X_cnt
    else:
        return

def xgb(config,X_cnt):
    type_indicators = list(config['model']['type_indicators'])

    pred=[]
    # Let's train type indicator individually
    for l in range(len(type_indicators)):

        model_path="data/models/"+str(l+1)+"_model.pickle.dat"
        xgb = open(model_path, 'rb')
        model = pickle.load(xgb)

        y_pred = model.predict_proba(X_cnt)
        pred_prob=y_pred
        pred.append(pred_prob)

    return pred


@app.route('/', methods=['GET', 'POST'])
def main():
    """Main view that shows the text box for input and displays the prediction results in a separate div"""
    try:
        if request.method == 'GET':
            return render_template('first_page.html')
        if request.method == 'POST':
            statement = str(request.form['statement'])

            processed = preprocess(statement,config)
            # load models

            count_vec=vectorize(config, processed)

            pred_type = list(xgb(config,count_vec))

            ie = "Introversion: "+str(round(pred_type[0][-1][0], 2)) + " / " + "Extroversion: "+str(round(pred_type[0][-1][1], 2))
            ns = "Intuition: "+str(round(pred_type[1][-1][0], 2)) + " / " + "Sensing: "+ str(round(pred_type[1][-1][1], 2))
            ft = "Feeling: "+str(round(pred_type[2][-1][0], 2)) + " / " + "Thinking: "+ str(round(pred_type[2][-1][1], 2))
            jp = "Judging: "+str(round(pred_type[3][-1][0], 2)) + " / " + "Perceiving: "+ str(round(pred_type[3][-1][1], 2))

            result={"I/E": ie, "N/S": ns, "F/T": ft, "J/P": jp}

            if (app.config['MODE'] == "AWS"):
                logger.debug("Adding new record to database in RDS.")
            else:
                logger.debug("Adding new record to the local database.")

            new_entry = mbti_1(
                Posts=statement,
                I=str(round(pred_type[0][-1][0], 2)),
                E=str(round(pred_type[0][-1][1], 2)),
                N=str(round(pred_type[1][-1][0], 2)),
                S=str(round(pred_type[1][-1][1], 2)),
                F=str(round(pred_type[2][-1][0], 2)),
                T=str(round(pred_type[2][-1][1], 2)),
                J=str(round(pred_type[3][-1][0], 2)),
                P=str(round(pred_type[3][-1][1], 2))
            )

            db.session.add(new_entry)
            db.session.commit()
            logger.debug("New record added to the database")
            logger.info('Prediction made and updated.')

            return render_template('first_page.html', original_input=statement, result=result)

    except:
        logger.warning('Error raised while rendering template.')

        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])



