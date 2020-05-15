import os
import sqlalchemy as sql
from sqlalchemy import text
from sqlalchemy import Integer, String, Float,Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import config
import pandas as pd
import logging
from tqdm import tqdm


def create_schema_models(Base):
    """
    Creates ORM models for tables within rds/sql database
    :param Base: This is the base model to build on top of
    :return `object`: ORM model classes
    """

    class Metacritic(Base):
        """
            Creates a datamodel for the Metacritic games database to be set up
        """
        __tablename__ = 'metacritic'
        id = Column(Integer, primary_key=True)
        Game = Column(String(100), nullable=False, unique=False)
        Genre = Column(String(100), nullable=False, unique=False)
        Metascore = Column(Float, nullable=False, unique=False)
        Userscore = Column(Float, nullable=False, unique=False)

        def __repr__(self):
            return '<Game {!r},MetaScore {!r},UserScore {!r}>'.format(self.Game, self.Genre, self.self.Metascore,
                                                                      self.Userscore)

    class Sales(Base):
        """
            Creates a datamodel for the Sales of games database to be set up
        """
        __tablename__ = 'sales'
        id = Column(Integer, primary_key=True)
        Game = Column(String(100), nullable=False, unique=False)
        Genre = Column(String(100), nullable=False, unique=False)
        NA_sales = Column(Float, nullable=False, unique=False)
        EU_sales = Column(Float, nullable=False, unique=False)
        JP_sales = Column(Float, nullable=False, unique=False)
        Other_sales = Column(Float, nullable=False, unique=False)
        Global_sales = Column(Float, nullable=False, unique=False)

        def __repr__(self):
            return '<Game {!r},Global_Sales {!r}>'.format(self.Game, self.Global_sales)

    class Steam(Base):
        """
            Creates a datamodel for the Steam games by users database to be set up
        """
        __tablename__ = 'steam'
        id = Column(Integer, primary_key=True)
        Userid = Column(Integer, nullable=False, unique=False)
        Game = Column(String(100), nullable=False, unique=False)
        Playtime = Column(Float, nullable=False, unique=False)

        def __repr__(self):
            return '<User {!r},Game {!r}>'.format(self.userid, self.game)

    class Customer(Base):
        """
        Creates a datamodel for the customers interacting with the app
        """
        __tablename__ = 'customer'
        id = Column(Integer, primary_key=True)
        customer_first_name = Column(String(100), nullable=False, unique=False)
        customer_last_name = Column(String(100), nullable=False, unique=False)
        customer_fav_game = Column(String(100), nullable=False, unique=False)
        customer_fav_genre = Column(String(100), nullable=False, unique=False)
        customer_time_spent = Column(Float, nullable=False, unique=False)
        customer_rating = Column(Integer, nullable=True, unique=False)

        def __repr__(self):
            return '<User {!r},Favorite_Game {!r}>'.format(self.customer_id, self.customer_fav_game)

    return Metacritic,Customer,Steam,Sales

def create_database(local):
    """
    Creates a rds or local sql database schema with tables and populates the data into the tables
    :param: local bool - check s3.config.py - local = True creates and populates local database games.db and persists else creates rds instance db
    :return: None
    """

    Base = declarative_base()
    # get schemas
    Metacritic,Customer,Steam,Sales=create_schema_models(Base)

    # define engine string
    if local:
        LOCAL_PATH = config.DATABASE_PATH
        engine_string = 'sqlite:///' + str(LOCAL_PATH)

    else:
        conn_type = config.connection_type
        user = config.user
        password = config.password
        host = config.host
        port = config.port
        database = os.environ.get("DATABASE_NAME")
        engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)

    #create engine
    engine = sql.create_engine(engine_string)

    Base.metadata.create_all(engine)


    # make session
    Session = sessionmaker(bind=engine)
    session = Session()
    # Delete anything that's already in the tables
    try:
        session.execute(text("DELETE FROM metacritic"))
        session.execute(text("DELETE FROM sales"))
        session.execute(text("DELETE FROM steam"))
        session.execute(text("DELETE FROM customer"))
    except:
        pass

    #define variables
    CLEAN_FILE_LIST=config.CLEAN_DATA_FILE_PATHS
    cleaned_metacritic = pd.read_csv(CLEAN_FILE_LIST[0]).set_index('id')
    cleaned_sales = pd.read_csv(CLEAN_FILE_LIST[1]).set_index('id')
    cleaned_steam = pd.read_csv(CLEAN_FILE_LIST[2]).set_index('id')

    # iterate through rows, add and commit for all 4 tables
    metacritic_list=[]
    for idx,features in tqdm(cleaned_metacritic.iterrows()):
            metacritic_sample=Metacritic(id=int(idx),Game=str(features['Game']), Genre=str(features['Genre']),Metascore=float(features['metascore']),
                                    Userscore=float(features['userscore']))
            metacritic_list.append(metacritic_sample)

    session.add_all(metacritic_list)

    session.commit()
    logging.info("Database created with Metacritic scored games table")

    sales_list=[]
    for idx,features in tqdm(cleaned_sales.iterrows()):

            sales_sample=Sales(id=int(idx),Game=str(features['Game']),Genre=str(features['Genre']),NA_sales=float(features['NA_Sales']),EU_sales=float(features['EU_Sales']),
                           JP_sales=float(features['JP_Sales']),Other_sales=float(features['Other_Sales']),Global_sales=float(features['Global_Sales']))
            sales_list.append(sales_sample)
    session.add_all(sales_list)

    session.commit()
    logging.info("Database created with Sales of games table")

    steam_list=[]
    for idx,features in tqdm(cleaned_steam.iterrows()):
        steam_sample = Steam(id=int(idx),Userid=str(features['userid']),Game=str(features['Game']),Playtime=str(features['playtime']))
        steam_list.append(steam_sample)
    session.add_all(steam_list)

    session.commit()
    logging.info("Database created with Steam PC games table")

    customer_sample=Customer(id=1,customer_first_name='John',customer_last_name='Doe',
                             customer_fav_game='FIFA 19',customer_fav_genre='Sports',customer_time_spent=5.0,customer_rating=8)

    session.add(customer_sample)
    session.commit()
    logging.info("Database created with Steam PC games table")

    session.close()








