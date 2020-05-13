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
        return





def run_loading_AWS(config, bucket_name):
    '''Fetches the data from the raw source and dumps it on the AWS S3 bucket provided

    All data is dumped at <s3-bucket-name>/data/raw

    Args:
        config: Config dictionary
        bucket_name: target bucket name used for all analysis

    Returns:
        None
    '''
    logger.debug('Running the run_loading_AWS function')

    s31 = boto3.client('s3')
    s32 = boto3.resource('s3')
    for object in s31.list_objects_v2(Bucket=config['load_data']['SOURCE_BUCKET'])['Contents']:
        try:
            copy_source = {'Bucket': config['load_data']['SOURCE_BUCKET'], 'Key': object['Key']}
            bucket = s32.Bucket(bucket_name)
            logger.info("Copying %s from bucket %s to bucket %s", object['Key'], config['load_data']['SOURCE_BUCKET'],
                        bucket_name)
            bucket.copy(copy_source, config['load_data']['save_location'] + object['Key'])
            logger.info("File successfully copied.")

        except Exception as e:
            logger.error(e)
            return


def load_data(args):
    '''Fetches the data from the raw source and dumps it at the location specified

    Args:
        args: Argparse args - includes args.where, args.bucket
            args.where: 'Local' or 'AWS'
            args.bucket (required if args.where = 'AWS'): S3 bucket for all analysis

    Returns:
        None
    '''
    logger.debug('Running the load_data function')

    with open(os.path.join("config", "config.yml"), "r") as f:
        config = yaml.safe_load(f)

    if args.where == "AWS":
        run_loading_AWS(config, args.bucket)

    elif args.where == "Upload":
        upload_file_s3(config)

    else:
        logger.error(
            'Kindly check the arguments and rerun. To understand different arguments, run `python run.py --help`')
        return