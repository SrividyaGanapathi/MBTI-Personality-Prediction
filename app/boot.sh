#!/usr/bin/env bash
python3 run1.py load_data
python3 run1.py create_db --where=Local
python3 run1.py preprocess
python3 run1.py vec_tfidf
python3 run1.py xgb_model
