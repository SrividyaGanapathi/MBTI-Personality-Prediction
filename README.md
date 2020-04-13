# MSiA423 MBTI TYPE 
### By Srividya Ganapathi
### QA - Bhavya Kaushik

<!-- toc -->
- [Project Charter](#Project-Charter)
- [Sprint Plan](#Sprint-Plan)
- [Icebox](#Icebox)


## Project Charter
<!-- toc -->
### Vision 
Identify the personality and characteristics of a person as indicated by the Myers-Briggs Type Indicator(MBTI) test by identifying the patterns in his/her writing style.

### Mission
The MBTI test is used in various domains everyday but recently, the validity of the test has been questioned because of unreliability in experiments surrounding it, along with other reasons. But it has still proven to be a very useful tool in a lot of areas, and the purpose of this dataset[https://www.kaggle.com/datasnaek/mbti-type] is to help see if any patterns can be detected in specific types and style of writing of people and if these patterns are indicative of a person's personality. This overall explores the validity of the test in analysing, predicting or categorising behaviour. 

### Content
This dataset contains over 8600 rows of data, on each row is a person’s:
 - Type (This persons 4 letter MBTI code/type)
 - A section of each of the last 50 things they have posted (Each entry separated by "|||" (3 pipe characters))

### Success Criteria
As mentioned earlier, the experiments are unreliable. In such psychological tests, even an accuracy of 70% is acceptable for the tool to be relied upon. With more examples, the model can learn furter, but presently the data is static and the user will select a few statements iteratively to know his/her personality type. The app will also take feedback on whether it was right or wrong which will be used to test accuracy. This leaves room for future improvement to the model by using the selected words for each personality type.

<!-- toc -->

## Initiatives 
* Models for extracting writing styles and patterns associated with each MBTI type.
* Deployment of the model to a Flask app
* Model for predicting the MBTI type from selected statements
* Improve accuracy of the predictive model by several user inputs.

## Sprint Planning
For the next 4 sprints (Each sprint of 2 weeks) the Initiatives are:

### Initiative 1: Models to extract writing styles and patterns associated with each MBTI type.

#### Epic-1: Exploratory Data Analysis and preprocessing.
   - Story 1: EDA of the Data
   - Story 2: Apply different embeddings to the data (Count vectorizer, word2vec, GloVe etc.)
     
#### Epic-2: Comparison of models 
   - Story 1: Build models like regression, random forest, LSTM, KNN etc. under cross validation to identify the best model.

### Initiative 2: Develop the front and back ends of the model

#### Epic-1: Build the front end Flask app
   - Story 1: Create the first page layout
   - Story 2: Design the user input layer
   - Story 3: Set connections to the backend servers
     
#### Epic-2: Set up the cloud server for the data using AWS RDS and S3

#### Epic-3: Performing sanity check using test cases

### Initiative 3 : Model to predict the MBTI type from selected statements
#### Epic-1: Choose statements available to the user
   - Story 1: Map sets of statements corresponding to each personality type.
   - Story 2: Set connections to the backend servers
   - Story 3: Create new dataset of selected stat
   
#### Epic-2: Predict personality type
   - Story 1: Create a new dataset of the statements selected by the user 
   - Story 2: Predict the personality based on the selected statements.
     
#### Epic-3: Accuracy Check 
   - Story 1: Receive the actual MBTI Type from the user as input
   - Story 2: Append this to the record of the current user.

#### Epic-3
* Build the front end app 
  - Create the first page layout
  - Design the user input layout
  - Set connections to the backend servers
* Performing sanity check using test cases

## Icebox
#### Epic-4
* Identify users who know their MBTI personality to try the app.
* Bulid a database of the statements selected, the predicted personality and the actual personality for checking the accuracy of the model.
* Fine tuning the model to increase accuracy.



----------------------------------------------------------------------------------------------------------------------------------------




- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app
### 1. Initialize the database 

#### Create the database with a single song 
To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create_db --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py create_db` creates a database at `sqlite:///data/tracks.db` with the initial song *Radar* by Britney spears. 
#### Adding additional songs 
To add an additional song:

`python run.py ingest --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py ingest` adds *Minor Cause* by Emancipator to the SQLite database located in `sqlite:///data/tracks.db`.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on 
##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/tracks.db'

```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/cmawer/Repos/2020-MSIA423-template-repository/data/tracks.db'
```


### 2. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "penny-lane"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 3. Run the Flask app 

To run the Flask app, run: 

```bash
python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.
