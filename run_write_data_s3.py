from config import config
from src.store_data_in_s3 import write_to_s3
from src.acquire_from_api import acquire_data,data_dictionary,games_dataframe
import yaml
import logging

logging.basicConfig(filename="./config/logging/run_write_data_s3.log")
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

if __name__=='__main__':

    CONFIGURATION_PATH = config.CONFIGURATION_PATH
    yaml_config = yaml.safe_load(open(CONFIGURATION_PATH))
    # S3 configurations
    bucket_name = yaml_config['acquire_from_s3']['bucket_name']
    access_key = config.S3_ACCESS_KEY_ID
    secret_key = config.S3_SECRET_ACCESS_KEY
    folder_path = config.RAW_DATA_FOLDER
    raw_files = config.RAW_DATA_FILENAMES

    #GET data from API
    DATA_PATH = config.DATA_PATH


    #Acquire data
    results = acquire_data(**yaml_config.get('acquire_from_api').get('acquire_data'))

    #Create a data default dict
    games_dict = data_dictionary(results, **yaml_config.get('acquire_from_api').get('data_dictionary'))

    games = games_dataframe(games_dict)

    games.to_pickle(DATA_PATH)
    logger.info('Data retrieved from api')

    # write to s3
    try:
        logging.info('Successfully found s3 bucket')
        write_to_s3(bucket_name, access_key, secret_key, folder_path, raw_files)
        logging.info('Successfully stored files on S3')
    except Exception as e:
        logging.error("Coudn't write to S3", e)



