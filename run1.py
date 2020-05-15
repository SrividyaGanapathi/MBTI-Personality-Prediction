"""
Enables the command line execution of multiple modules within src/
This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.
To understand different arguments, run `python run.py --help`
"""
import os
import argparse
import logging
import logging.config
import yaml

with open(os.path.join("config", "config.yml"), "r") as f:
    config = yaml.safe_load(f)

# The logging configurations are called from local.conf
logging.config.fileConfig(os.path.join("config", "local.conf"))
logger = logging.getLogger(config['logging']['LOGGER_NAME'])

from src.load_data import load_data
from src.create_db import create_db

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run components of the run source code")
    subparsers = parser.add_subparsers()

    # Sub-parser for loading the raw data
    sb_fetch = subparsers.add_parser("load_data", description="Fetch the raw data from the source")
    sb_fetch.set_defaults(func=load_data)

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database to track usage logs")
    sb_create.add_argument("--where", default="Local",
                           help="'Local' or 'AWS'. Seeks variables from environment for AWS by default")
    sb_create.set_defaults(func=create_db)



    args = parser.parse_args()
    args.func(args)