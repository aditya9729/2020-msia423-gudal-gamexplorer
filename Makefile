data/external/games_data.pkl: config/config.yaml
	python3 run_pipeline.py acquire_from_s3 --config=config/config.yaml

data/external/intermediate.pkl data/external/features.npy: data/external/games_data.pkl config/config.yaml
	python3 run_pipeline.py featurize --config=config/config.yaml

data/external/train.npy data/external/test.npy models/als_model.joblib: data/external/features.npy data/external/intermediate.pkl config/config.yaml
	python3 run_pipeline.py train --config=config/config.yaml

models/model_metrics.txt: data/external/train.npy data/external/test.npy models/als_model.joblib config/config.yaml
	python3 run_pipeline.py score --config=config/config.yaml


pipeline: data/external/games_data.pkl data/external/intermediate.pkl data/external/features.npy data/external/train.npy data/external/test.npy models/als_model.joblib models/model_metrics.txt

app:
	python3 app.py

tests:
	pytest run_pipeline.py test

.PHONY: pipeline app tests
