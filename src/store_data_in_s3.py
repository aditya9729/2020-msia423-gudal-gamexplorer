import boto3
from tqdm import tqdm
import logging

# WRITE DATA TO S3
def write_to_s3(bucket_name,access_key,secret_key,folder,files):
	"""Writes data to the s3 bucket or stores in s3
	:param bucket_name `str`: AWS s3 bucket name
	:param access_key `str`: AWS access key id
	:param secret_key `str`: AWS secret key
	:param folder `str`: Folder containing the files to be uploaded
	:param files `str`: files to be uploaded
	:return: None
	"""
	try:
		s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
		logging.debug('Successfully found s3 bucket')
	except Exception as error1:
		logging.error(" Couldn't find the S3 bucket, check aws credentials and try again",error1)

	files_to_upload= files

	# upload files to s3
	try:
		for file in tqdm(files_to_upload):
			logging.debug('Writing files to S3')
			s3.upload_file(str(folder)+str(file),str(bucket_name), str(file))
	except Exception as error2:
		logging.error("Couldn't find files in the folder given to write to S3",error2)







