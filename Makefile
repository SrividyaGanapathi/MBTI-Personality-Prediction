load_data:
	python3 run1.py load_data

create_db:
	python3 run1.py create_db --where=Local

preprocess:
	python3 run1.py preprocess

vec_tfidf:
	python3 run1.py vec_tfidf

xgb_model:
	python3 run1.py xgb_model


all: load_data create_db preprocess vec_tfidf xgb_model

.PHONY: all