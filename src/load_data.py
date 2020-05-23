"""
This module contains functions to load the raw data from the source and dump it into the desired location
"""
import os
import logging
import boto3
import yaml
logger = logging.getLogger()


def upload_file_s3(config):
    '''Fetches the data from the local source and dumps it into the s3 bucket


    Args:
        config: Config dictionary

    Returns:
        None
    '''

    logger.debug('Running the upload_file function')
    try:

        s3 = boto3.resource('s3')
        Bucket=config['load_data']['SOURCE_BUCKET']

        s3.Bucket(Bucket).upload_file(config['load_data']['local_location'], "dump/mbti_1.csv")

    except Exception as e:
        logger.error(e)
        print(e)
        return

def load_data(args):
    '''Fetches the data from the raw source and dumps it at the location specified

    Args:
        None

    Returns:
        None
    '''
    logger.debug('Running the load_data function')
    try:

        with open(os.path.join("config", "config.yml"), "r") as f:
            config = yaml.safe_load(f)

        upload_file_s3(config)
        print("Uploaded data successfully")

    except Exception as e:
        logger.error(e)
        print(e)
        return

