import os
MODE='Local' #'Local' or 'AWS' #change as necessary
BUCKET_NAME='nw-srividyaganapathi-s3' #Necessary if MODE = 'AWS'

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "mbti"
HOST = "0.0.0.0"

conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = 'msia423-srividya.cyzkqezn0z0w.us-east-2.rds.amazonaws.com'
port = 3306
DATABASE_NAME = 'msia423_db'

if MODE == 'AWS':
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".\
    format(conn_type, user, password, host, port, DATABASE_NAME)
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/msia423_db.db'

#SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False
