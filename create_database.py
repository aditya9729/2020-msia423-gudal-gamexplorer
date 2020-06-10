from config import changeable_config
from src.customer_database import create_database

import logging.config

logging.basicConfig(filename="./config/logging/create_database.log")

logger = logging.getLogger(__name__)

logger.setLevel("INFO")


if __name__=="__main__":

    local=changeable_config.local
    try:
        create_database(local)
        logging.info('Schema for database created')
    except Exception as e:
        logging.error("Couldn't create schema", e)
