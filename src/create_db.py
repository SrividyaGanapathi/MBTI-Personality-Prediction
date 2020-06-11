"""
This module contains functions to create the database to log usage data
"""

import os
import logging
import logging.config

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import pandas as pd

import yaml
import argparse

import getpass

logger = logging.getLogger()

Base = declarative_base()


class mbti_1(Base):
    """ Defines the data model for the table `mbti_1`. """

    __tablename__ = 'mbti_1'

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    Posts = Column(String(20000), unique=False, nullable=False)
    I = Column(String(2), unique=False, nullable=False)
    E = Column(String(2), unique=False, nullable=False)
    N = Column(String(2), unique=False, nullable=False)
    S = Column(String(2), unique=False, nullable=False)
    F = Column(String(2), unique=False, nullable=False)
    T = Column(String(2), unique=False, nullable=False)
    J = Column(String(2), unique=False, nullable=False)
    P = Column(String(2), unique=False, nullable=False)


    def __repr__(self):
        mbti_repr = "<mbti_1=(Type='%s Posts='%d>"
        return mbti_repr % (self.Posts,self.I,self.E,self.N,self.S,self.F,self.T,self.J,self.P)

def create_db(args):
    """Creates a database with the data models inherited from `Base` (mbti_1).
    Args:
        args: Argparse args - include args args.where
            args.where:  'Local' or 'AWS'
    Returns:
        None
    """
    with open(os.path.join("config", "config.yml"), "r") as f:
        config = yaml.safe_load(f)

    logger.debug('Running the create_db function')

    if args.where == "Local":
        try:
            logger.info('Creating a local database at {}'.format(config['db_config']['SQLALCHEMY_DATABASE_URL']))
            engine = create_engine(config['db_config']['SQLALCHEMY_DATABASE_URL'])
            logger.debug('Database engine successfully created.')
        except Exception as e:
            logger.error(e)

    elif args.where == "AWS":
        try:

            logger.info(
                'Creating an RDS database based on environment variables: MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB.')
            conn_type = "mysql+pymysql"
            user = os.getenv("MYSQL_USER")
            password = os.getenv("MYSQL_PASSWORD")
            host = config['rds']['MYSQL_HOST']
            port = config['rds']['MYSQL_PORT']
            db_name = config['rds']['MYSQL_DB']
            engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, db_name)

            logger.debug('Creating database now.')
            engine = create_engine(engine_string)
            logger.debug('Database engine successfully created.')

        except Exception as e:
            logger.error("Database engine cannot be created. Kindly check the configurations and try again.")
            logger.error(e)

    else:
        raise ValueError(
            'Kindly check the arguments and rerun. To understand different arguments, run `python run1.py --help`')

    if args.where in ["AWS", "Local"]:

        try:
            Base.metadata.create_all(engine)
            logger.info('Database successfully created.')


        except Exception as e:
            logger.error("Database could not be created. Kindly check the configurations and try again.")
