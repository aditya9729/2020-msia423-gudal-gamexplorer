import os
import sqlalchemy as sql
from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
from config import changeable_config
import logging.config
import sys

logging.basicConfig(filename="./config/logging/customer_database.log")

logger = logging.getLogger(__name__)

logger.setLevel("INFO")

Base = declarative_base()

class Customer(Base):
    """
    Creates a datamodel for the customers interacting with the app
    """
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    favorite_game = Column(String(100), nullable=False, unique=False)
    reco_game1 = Column(String(100), nullable=False, unique=False)
    reco_game2 = Column(String(100), nullable=False, unique=False)
    reco_game3 = Column(String(100), nullable=False, unique=False)
    reco_game4= Column(String(100), nullable=False, unique=False)
    reco_game5 = Column(String(100), nullable=False, unique=False)
    reco_game6 = Column(String(100), nullable=False, unique=False)
    reco_game7 = Column(String(100), nullable=False, unique=False)
    reco_game8 = Column(String(100), nullable=False, unique=False)
    reco_game9 = Column(String(100), nullable=False, unique=False)
    reco_game10 = Column(String(100), nullable=False, unique=False)

    def __repr__(self):
        return '<Favorite_Game {!r}>'.format(self.favorite_game)



def create_database(local):
    """
    Creates a rds or local sql database schema with tables and populates the data into the tables
    :param: local bool - check s3.changeable_config.py - local = True creates and populates local database games.db and persists else creates rds instance db
    :return: None
    """


    # define engine string
    if local:
        LOCAL_PATH = changeable_config.DATABASE_PATH
        engine_string = 'sqlite:///' + str(LOCAL_PATH)

    else:
        conn_type = changeable_config.connection_type
        user = changeable_config.user
        password = changeable_config.password
        host = changeable_config.host
        port = changeable_config.port
        database = os.environ.get("DATABASE_NAME")
        engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)

    #create engine

    try:
        engine = sql.create_engine(engine_string)

        Base.metadata.create_all(engine)

    except Exception as e:
        logger.error("Couldn't create database check engine string or connection",e)
        sys.exit('exit')













