import os

#Flask app configs
DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5000
APP_NAME = "game-recommender"

SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = True  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

# Database engine Connection string

# For CREATING Local Database connection config
local=True # change this for local sqlite vs rds instance database, don't forget to set env variables see above
PROJECT_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # change be changed
DATABASE_PATH = os.path.join(PROJECT_HOME, 'data/customers.db')# name is customers.db by default


# RDS instance Database configurations
connection_type="mysql+pymysql" # for rds
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
database = os.environ.get("MYSQL_DATABASE")

## This is to write data to RDS/local database
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
if SQLALCHEMY_DATABASE_URI is not None:
    pass
elif host is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/customers.db'
else:
    SQLALCHEMY_DATABASE_URI = '{dialect}://{user}:{pw}@{host}:{port}/{db}'.format(dialect=DB_DIALECT, user=DB_USER,
                                                                                  pw=DB_PW, host=DB_HOST, port=DB_PORT,
       
SAVE_INTERMEDIATE_PATH='./data/external/intermediate.pkl'
SAVE_MODEL_PATH='./models/als_model.joblib'

# aws S3 Credentials
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Configurations for src/acquire_from_api.py script to store data into s3
RAW_DATA_FOLDER = "./data/external/"
RAW_DATA_FILENAMES=['games_data.pkl']
RAW_DATA_WRITE_LOCATION = "./data/external/"

## Configuration paths for src/featurize.py
DATA_PATH = './data/external/games_data.pkl'
SAVE_INTERMEDIATE_PATH = './data/external/intermediate.pkl'
SAVE_FEATURES_PATH = './data/external/features.npy'

#Configuration paths for src/train_model.py
FEATURES_PATH = './data/external/features.npy'

SAVE_TRAIN_PATH = './data/external/train.npy'

SAVE_TEST_PATH = './data/external/test.npy'

SAVE_MODEL_PATH = './models/als_model.joblib'

# configurations paths for src/score_model.py
MODEL_METRICS_PATH='./models/model_metrics.txt'

# unchangeable YAML Configurations path
CONFIGURATION_PATH = './config/config.yaml'
