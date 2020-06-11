# MSiA423 Project Repositiory
## MBTI Assessment App
### By Srividya Ganapathi
### QA - Bhavya Kaushik

<!-- toc -->
- [Project Charter](#Project-Charter)
- [Sprint Plan](#Sprint-Planning)
- [Backlog](#Backlog)
- [Icebox](#Icebox)
- [Running the application](#running-the-application)
  * [1. Initial setup](#1-initial-setup)
  * [2. Download the data](#2-download-the-data)
  * [3. Run the pipeline](#3-Run-the-pipeline)
  * [4. Run the App](#4-Run-the-App)
  
- [Logging](#logging)



## Project Charter
<!-- toc -->
### Vision 
The Myers Briggs Type Indicator (or MBTI for short) is a popular personality test that divides everyone into 16 distinct personality types. Companies use it to analyze job applicants, managers use it to determine which employees might get along with one another, and your friends might use it to tell the world what kind of person they are.
The objective of this project is to identify the personality and characteristics of a user as indicated by the MBTI test using patterns in the user's chosen statements or writing styles.

### Mission
The MBTI test is used in various domains like business, medicine and others everyday but recently, the validity of the test has been questioned because of unreliability in experiments surrounding it, along with other reasons. But it has still proven to be a very useful tool in a lot of areas, and the purpose of this dataset [https://www.kaggle.com/datasnaek/mbti-type] is to help see if any patterns can be detected in specific types and style of writing of people and if these patterns are indicative of a person's personality. A machine learning predictive model will be developed to classify a user into a personality type. The model will be hosted and a web application interface will be created for the users. This overall explores the validity of the test in analysing, predicting or categorising behaviour. 

### Content
This dataset contains over 8600 rows of data, on each row is a person’s:
 - Type (This persons 4 letter MBTI code/type)
 - A section of each of the last 50 things they have posted (Each entry separated by "|||" (3 pipe characters))

### Success Criteria
- The success criterion for the model performance evaluation would be the classification accuracy.
In such psychological tests, even an accuracy of 50% is acceptable for the tool to be relied upon. The app will take feedback on whether it was right or wrong which will also be used to test accuracy.  
- The business outcome will be measured by the perusal of the app by third parties or business stakeholders to delve deeper into an individual's personality using their social media activity.
- User engagement and agreement with their personality assessment is also a success criterion.

<!-- toc -->

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
#### Epic-1: Curate statements for the user to choose from
   - Story 1: Map sets of statements corresponding to each personality type.
   - Story 2: Set connections to the backend servers
   
#### Epic-2: Predict personality type
   - Story 1: Create a new dataset of the statements selected by the user 
   - Story 2: Predict the personality based on the selected statements.
   
### Initiative 4 : Fine tuning the model to increase accuracy 

#### Epic-1: Accuracy Check 
   - Story 1: Receive the actual MBTI Type from the user as input
   - Story 2: Append this to the record of the current user.
   - Story 3: For every few use cases append the record to the train data.

#### Epic-2: Finetuning the model
  - Story 1: Penalize the statements that led to a misclassification.
  - Story 2: Retrain the model to increase accuracy.
  
## Backlog

The story points are assigned as follows:
-   0 points - quick chore
-   1 point ~ 1 hour (small)
-   2 points ~ 1/2 day (medium)
-   4 points ~ 1 day (large)
-   8 points - big and needs to be broken down more when it comes to execution 


1. Initiative1.Epic1.Story1  (4) [Planned]
2. Initiative1.Epic1.Story2  (4) [Planned]
3. Initiative1.Epic2.Story1  (8) [Planned]
4. Initiative2.Epic1.Story1  (8) [Planned]
5. Initiative2.Epic1.Story2  (2) [Planned]
6. Initiative2.Epic1.Story3  (2) [Planned]
7. Initiative2.Epic2         (1) [Planned]
8. Initiative2.Epic3         (2) [Planned]
9. Initiative3.Epic1.Story1  (2) [Planned]
10. Initiative3.Epic1.Story2 (2) [Planned]
11. Initiative3.Epic2.Story1 (8) [Planned]
12. Initiative3.Epic2.Story2 (1) [Planned]


## Icebox

* Initiative4          




## Running the application

### 1. Initial Setup

To run the app, ensure to go through the following:
* Docker desktop should be running
* Set up AWS CLI. Kindly refer to this [link](https://www.kaggle.com/datasnaek/mbti-type/download).
* Set the following environment variables with the following commands in command line:
```bash
    export AWS_ACCESS_KEY_ID=""
    export AWS_SECRET_ACCESS_KEY=""
    export AWS_DEFAULT_REGION=""
```


### 2. Download the data

Original Data Source: [Kaggle](https://www.kaggle.com/datasnaek/mbti-type/download)

The data has been placed in the S3 bucket named nw-srividyaganapathi-s3 from where it can 
be downloaded. The steps for the same are mentioned below.


### 3. Run the pipeline 
The following commands will accomplish these tasks - 
- Load Data - The data will be loaded from the S3 bucket to
the local location(both mentioned in the config). 
`--where= Upload/Download` in **boot.sh** will upload data to S3 bucket or download data from S3 bucket
- Create DB -This function will let you create a database in either local system or
RDS. `--where= Local/AWS` in **boot.sh** will create a database locally or on RDS.
- Preprocess - Preprocessing
- Vectorize - Vectorization
- XGBoost - XGBoost model

#### Docker Image
Build the docker image with the following command in command line:
```bash
docker build -t mbti .
```
#### Pipeline
Run **boot.sh** file through the docker image with the aws credentials using the following command in command line.
```bash
winpty docker run -v "$(pwd)":"$(pwd)" -it --env AWS_ACCESS_KEY_ID --env AWS_SECRET_ACCESS_KEY mbti boot.sh
```
#### Testing
Run the **test/runtests.sh** file through the docker image using the following command in command line.
```bash
winpty docker run mbti test/runtests.sh
```
This will run the tests on preprocessing, vectorizing and modelling.

Note: If you are a MAC user, please remove the `winpty`.


### 4. Run the App

The app will be built separately. It can update user inputs and 
the corresponding predictions either in the local db or in RDS.

To choose the table where the rows will be updated set the MODE in 
**config/flaskconfig.py** to Local/AWS.

Note: If you choose Local(AWS) for Pipeline, choose Local(AWS) for the app and 

#### Docker Image
Build the docker image with the following command in command line:
```bash
docker build -f app/Dockerfile -t mbti_app .
```
#### Deployment
Run the following command in command line to start the app:
```bash
winpty sh app/boot_app.sh
```
Note: If you are a MAC user, please remove the `winpty`.

#### Kill Container
Once finished with the app, you will need to kill the container. To do so:
```bash
docker kill testapp 
```
Where `testapp` is the name given in the docker run command.


## Logging
All logs are saved at **logs/logfile.log** in the docker container.


## Acknowledgements
Sincerest thanks:  
* Bhavya Kaushik
* Chloe Mawer
* Fausto Inestroza
* Jaehoon Koo






----------------------------------------------------------------------------------------------------------------------------------------


