import yaml
import logging.config
from src.acquire_from_s3 import download_data
from src.featurize import featurize
from src.train_model import compute_similarity,train_test_split,train_model
from src.score_model import score_model,evaluate_model,save_model_metrics
from src.store_data_in_s3 import write_to_s3
from src.acquire_from_api import acquire_data, data_dictionary, games_dataframe
import joblib
from config import config
import numpy as np
import pandas as pd
import argparse
import sys
from test import run_tests

logging.basicConfig(filename="./config/logging/run_pipeline.log")

logger = logging.getLogger(__name__)

logger.setLevel("INFO")


if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Acquire from s3, clean, create features, train and score model for a game recommender")

    parser.add_argument('step', help='Which step to run', choices=['acquire_from_api','write_to_s3',
                                                                   'acquire_from_s3','featurize','train','score','test'])
    parser.add_argument('--input', '-i', default=None, help='Path to input data (optional,default=None)')
    parser.add_argument('--config', default=None, help='Path to configuration file')
    parser.add_argument('--output', '-o', default=None, help='Path to save output file (optional, default = None)')

    args = parser.parse_args()

    # Load configuration file for parameters and tmo path
    with open(args.config, "r") as f:
        yaml_config = yaml.load(f, Loader=yaml.FullLoader)

    logger.info("Configuration file loaded from %s" % args.config)

    # S3 configurations
    bucket_name = yaml_config['acquire_from_s3']['bucket_name']
    access_key = config.AWS_ACCESS_KEY_ID
    secret_key = config.AWS_SECRET_ACCESS_KEY
    folder_path = config.RAW_DATA_FOLDER
    raw_files = config.RAW_DATA_FILENAMES

    # GET data from API

    if args.step=='acquire_from_api':

        DATA_PATH = config.DATA_PATH

        results = acquire_data(**yaml_config.get('acquire_from_api').get('acquire_data'))

        games_dict = data_dictionary(results, **yaml_config.get('acquire_from_api').get('data_dictionary'))

        games = games_dataframe(games_dict)

        games.to_pickle(DATA_PATH)
        logger.info('Data retrieved from api')
    # write to s3
    if args.step=='write_to_s3':

        try:
            logging.info('Successfully found s3 bucket')
            write_to_s3(bucket_name, access_key, secret_key, folder_path, raw_files)
            logging.info('Successfully stored files on S3')
        except Exception as e:
            logging.error("Coudn't write to S3", e)



    if args.step == 'acquire_from_s3':
        # change this to your own bucket name
        bucket_name = yaml_config['acquire_from_s3']['bucket_name']
        # raw data to save
        s3_file_name = yaml_config['acquire_from_s3']['s3_file_name']
        if args.output is None:
            # data path to save in
            save_path = yaml_config['acquire_from_s3']['save_path']

        if args.output is not None:
            save_path=args.output
            logger.info("Output saved to %s" % args.output)


        # fetch data and save into s3
        download_data(bucket_name, s3_file_name, save_path)

    # FEATURIZE data
    elif args.step == 'featurize':
        # featurize_data configuration paths

        # Featurize the data and save the intermediate data and featurized array
        try:
            if args.input is not None:
                DATA_PATH=args.input
                data = pd.read_pickle(DATA_PATH)
                logger.info('Input data loaded from %s', args.input)
            else:
                DATA_PATH = yaml_config['featurize_paths']['DATA_PATH']
                data = pd.read_pickle(DATA_PATH)
            SAVE_INTERMEDIATE_PATH =yaml_config['featurize_paths']['SAVE_INTERMEDIATE_PATH']
            SAVE_FEATURES_PATH =yaml_config['featurize_paths']['SAVE_FEATURES_PATH']
        except Exception as e:
            logger.error(f"Data doesnot exist in {args.input}",e)
            sys.exit('exit')


        features_array, saved_data = featurize(data, **yaml_config.get('featurize'))

        saved_data.to_pickle(SAVE_INTERMEDIATE_PATH)
        logger.info('Saved intermediate data to be used for recommendations')

        try:
            if args.output is not None:
                SAVE_FEATURES_PATH=args.output
                np.save(SAVE_FEATURES_PATH, features_array)
                logger.info("Output saved to %s" % args.output)
                logger.info('Features array saved and ready to be fed to model')

            else:
                np.save(SAVE_FEATURES_PATH, features_array)
                logger.info('Features array saved and ready to be fed to model')

        except Exception as e:
            logger.error(f"Path {args.output} doesnot exist, also please check if the saved file is a "
                         f"numpy array",e)
            sys.exit('exit')


    elif args.step=='train':
        # Training the model
        try:
            if args.input is not None:
                FEATURES_PATH=args.input
                features = np.load(FEATURES_PATH)
                logger.info('Input data loaded from %s', args.input)
            else:
                FEATURES_PATH =yaml_config['train_model']['file_paths']['FEATURES_PATH']
                features = np.load(FEATURES_PATH)
                FEATURES_PATH = yaml_config['train_model']['file_paths']['FEATURES_PATH']

        except Exception as e:
            logger.error(f"Data does-not exist in {args.input}, also check if it a numpy array",e)
            sys.exit('exit')
        # get path configurations



        # Train model now and save train,test and model
        features = np.load(FEATURES_PATH)
        cosine_sim = compute_similarity(features)
        logger.info('Cosine Similarity computed successfully')
        train, test = train_test_split(cosine_sim, **yaml_config.get('train_model').get('train_test_split'))
        logger.info('Train test split done successfully')

        SAVE_TRAIN_PATH = yaml_config['train_model']['file_paths']['SAVE_TRAIN_PATH']
        SAVE_TEST_PATH = yaml_config['train_model']['file_paths']['SAVE_TEST_PATH']
        np.save(SAVE_TRAIN_PATH, train)
        np.save(SAVE_TEST_PATH, test)
        model = train_model(train, **yaml_config.get('train_model').get('train_model'))
        logger.info('Model trained successfully')

        try:
            if args.output is not None:
                SAVE_MODEL_PATH = args.output

                joblib.dump(model, SAVE_MODEL_PATH)

                logger.info("Output saved to %s" % args.output)
                logger.info(f'Model saved to {SAVE_MODEL_PATH} successfully')

            else:
                SAVE_MODEL_PATH = yaml_config['train_model']['file_paths']['SAVE_MODEL_PATH']
                joblib.dump(model, SAVE_MODEL_PATH)
                logger.info(f'Model saved to {SAVE_MODEL_PATH} successfully')

        except Exception as e:
            logger.error(f"Path {args.output} doesnot exist, also please check if the saved file is a "
                         f"joblib file", e)
            sys.exit('exit')



    # Scoring the model
    elif args.step=='score':

        try:
            if args.input is not None:


                SAVE_MODEL_PATH = args.output

                model = joblib.load(SAVE_MODEL_PATH)

                logger.info("Output saved to %s" % args.input)
                logger.info(f'Model saved to {SAVE_MODEL_PATH} successfully')

            else:
                SAVE_MODEL_PATH = yaml_config['score_model']['file_paths']['SAVE_MODEL_PATH']

                model = joblib.load(SAVE_MODEL_PATH)
                logger.info(f'Model saved to {SAVE_MODEL_PATH} successfully')

        except Exception as e:
            logger.error(f"Path {args.output} doesnot exist, also please check if the saved file is a "
                         f"joblib file", e)
            sys.exit('exit')

        MODEL_PATH = SAVE_MODEL_PATH
        TEST_PATH = yaml_config['score_model']['file_paths']['SAVE_TEST_PATH']

        predictions = score_model(model)
        logger.info('Model scored successfully')

        actual_test = np.load(TEST_PATH)
        metrics_tuple = evaluate_model(predictions, actual_test)
        logger.info('Model evaluated successfully')

        MODEL_METRICS_PATH = yaml_config['score_model']['file_paths']['MODEL_METRICS_PATH']
        save_model_metrics(MODEL_METRICS_PATH, metrics_tuple)
        logger.info(f'Saved the model metrics to {MODEL_METRICS_PATH}')

        logger.info('Model pipeline built')

    # run tests
    else:
        run_tests(args)



