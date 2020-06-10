import boto3
import sys
import logging.config
import os

logging.basicConfig(filename="./config/logging/run_pipeline.log")
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def download_data(bucket_name,download_file,save_path):
    """Downloads data from S3 bucket and saves in the file path given
    :param bucket_name `str`: S3 bucket name
    :param download_file `str`: File to download
    :param save_path `str`: Path to store the data in
    :return `dataframe`: Data to be used to create features
    """
    if not isinstance(bucket_name, str):
        logger.error("Bucket name is not a string")
        sys.exit('exit')

    if not isinstance(download_file, str):
        logger.error("download_file is not a string")
        sys.exit('exit')

    if not isinstance(save_path, str):
        logger.error("save_path is not a string")
        sys.exit('exit')

    try:

        if os.path.exists(save_path):
            logger.info(f"{save_path} exists, can save the file.")

        else:
            logger.warning(f"{save_path} does not exist, cannot save the file.")

    except Exception as e:
        logger.error(f"{save_path} does not exist, please change file name or make a path",e)
        sys.exit('exit')


    try:
        s3 = boto3.client('s3')

        logger.info(f"S3 Bucket: {bucket_name} found")
    except Exception as e:
        logger.error(f"S3 Bucket: {bucket_name} cannot be found, try a different one",e)
        sys.exit('exit')

    try:
        s3.download_file(bucket_name,download_file,save_path)#download data from s3
        logger.info(f'File {download_file} from S3 Bucket: {bucket_name} was successfully downloaded')
    except Exception as e:
        logger.error(f'Could not download {download_file} from S3 Bucket: {bucket_name}, please try again',e)
        sys.exit('exit')



