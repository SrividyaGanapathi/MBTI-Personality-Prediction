#!/bin/bash
#Loads data to or from S3. Help in run1.py
python3 run1.py load_data --where=Download
# Creates database in local or RDS. Help in run1.py
python3 run1.py create_db --where=Local
#Preprocesses raw data
python3 run1.py preprocess
#Vectorizes preprocessed data
python3 run1.py vec
# Fits xgb models for each type indicator
python3 run1.py xgb_model

