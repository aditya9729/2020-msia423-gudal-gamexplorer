from src.game_database import create_database
from src.clean_data import read_data,filter_data,save_files
from config import config

from tqdm import tqdm

import logging

if __name__=='__main__':

    # set up configuration variables
    df_names = config.PROCESS_DATAFRAMES
    CLEAN_PATH=config.CLEAN_DATA_WRITE_LOCATION

    files = config.RAW_DATA_FILENAMES
    write_location = config.RAW_DATA_WRITE_LOCATION
    folder_path = config.RAW_DATA_FOLDER

    local=config.local

    # read data and process data
    try:
        logging.info('Ingesting files')
        ingested_files = read_data(folder_path , df_names)
        logging.info('Ingested all files')
    except Exception as e:
        logging.error("Couldn't complete ingestion, try again",e)

    # clean data from the ingested files
    cleaned_files = {}
    try:
        logging.info('Cleaning files')
        for file in tqdm(ingested_files.keys()):
            cleaned_files=filter_data(file,ingested_files,cleaned_files)
        logging.info('Cleaning complete')
    except Exception as e:
        logging.error("Couldn't complete cleaning, try again",e)

    # save files into data/clean/
    try:
        logging.info('Saving files')
        for file in tqdm(cleaned_files.keys()):
            save_files(file,CLEAN_PATH,cleaned_files)
        logging.info('Saved files')
    except Exception as e:
        logging.error("Couldn't save files",e)

    # Create schema and database
    try:
        create_database(local)
        logging.info('Schema for database created')
    except Exception as e:
        logging.error("Couldn't create schema", e)
