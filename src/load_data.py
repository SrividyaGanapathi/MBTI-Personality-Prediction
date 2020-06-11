"""
This module contains functions to load the raw data from the source and dump it into the desired location
"""
import os
import logging
import boto3
import yaml
from botocore.exceptions import ClientError
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

        s3.Bucket(Bucket).upload_file(config['load_data']['local_location'], "mbti_1.csv")

    except Exception as e:
        logger.error(e)
        return


def download_file_s3(config):
    '''Fetches the data from the s3 bucket and dumps it into the local source


    Args:
        config: Config dictionary

    Returns:
        None
    '''

    logger.debug('Running the download_file function')
    s3 = boto3.client('s3')
    for object in s3.list_objects_v2(Bucket=config['load_data']['SOURCE_BUCKET'])['Contents']:
        try:
            logger.info("Downloading %s from bucket %s", object['Key'], config['load_data']['SOURCE_BUCKET'])
            s3.download_file(config['load_data']['SOURCE_BUCKET'], object['Key'],
                             os.path.join("data", "raw", object['Key']))
            logger.info("File successfully downloaded to %s", os.path.join("data", "raw"))

        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                logger.warning("The object %s does not exist in AWS bucket %s.", object['Key'],
                               config['load_data']['SOURCE_BUCKET'])
            else:
                raise

        except Exception as e:
            logger.error(e)
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

        if args.where == "Download":
            download_file_s3(config)
            logger.debug("Downloaded data successfully")

        elif args.where =="Upload":
            upload_file_s3(config)
            logger.debug("Uploaded data successfully")

    except Exception as e:
        logger.error(e)
        return

