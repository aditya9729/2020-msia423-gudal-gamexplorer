
from config import config
from src.store_data_in_s3 import  write_to_s3
import logging

if __name__=='__main__':

    # s3 configs
    bucket_name = config.S3_BUCKET_NAME
    access_key = config.S3_ACCESS_KEY
    secret_key = config.S3_SECRET_KEY
    folder_path = config.RAW_DATA_FOLDER
    raw_files = config.RAW_DATA_FILENAMES

    # write to s3
    try:
        logging.info('Successfully found s3 bucket')
        write_to_s3(bucket_name, access_key, secret_key, folder_path, raw_files)
        logging.info('Successfully stored files on S3')
    except Exception as e:
        logging.error("Coudn't write to S3", e)



