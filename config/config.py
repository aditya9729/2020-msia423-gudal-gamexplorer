import os

# Configurations to run py script to store data into s3
PROCESS_DATAFRAMES=['metacritic','sales','steam']
RAW_DATA_FOLDER = "./data/external/"
RAW_DATA_FILENAMES=['metacritic.csv','sales.csv','steam.csv']
RAW_DATA_WRITE_LOCATION = "./data/external/"

# Configurations to clean data
CLEAN_DATA_WRITE_LOCATION='./data/clean/'
CLEAN_DATA_FILES=['cleaned_metacritic.csv','cleaned_sales.csv','cleaned_steam.csv']
CLEAN_DATA_FILE_PATHS=[CLEAN_DATA_WRITE_LOCATION+str(file) for file in CLEAN_DATA_FILES]

# aws S3 Credentials
S3_BUCKET_NAME = 'nw-adityagudal-s3' # change this to your own bucket na,e
S3_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
S3_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')


# RDS instance Database configurations
connection_type="mysql+pymysql" # for rds
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
database = os.environ.get("DATABASE_NAME")


# Local Database connection config
local=False # change this for local sqlite vs rds instance database, don't forget to set env variables see above
PROJECT_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # change be changed
DATABASE_PATH = os.path.join(PROJECT_HOME, 'data/games.db')# name is games.db by default