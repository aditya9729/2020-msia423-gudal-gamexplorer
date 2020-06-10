import pandas as pd
import sys
import logging.config
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import StandardScaler

logging.basicConfig(filename="./config/logging/run_pipeline.log")

logger = logging.getLogger(__name__)

logger.setLevel("INFO")

def get_genres(genres):
    """Converts genre list of dictionaries into list of genres - simplification
    :param genres `list`: genres list of dictionaries
    :return: list of genres for each game
    """
    if not isinstance(genres, list):
        logger.error("genres is not a list instance")
        sys.exit('exit')

    # extract the genre names
    try:

        genres_list = []
        if genres:
            for genre in genres:
                genres_list.append(genre['name'])

        else:
            genres_list.append('Unknown')

        logger.info('Successfully converted genre dictionary into a list')

    except Exception as e:
        print('Not a list')
        logger.error("Could not convert genres dictionary to a list, try again",e)
        sys.exit('exit')


    return genres_list

def get_stores(stores):
    """Converts stores list of dictionaries into stores- simplification
    :param stores `list`: stores list of dictionaries
    :return: first store for each game
    """

    if not isinstance(stores, list):
        logger.error("stores is not a list instance")
        sys.exit('exit')

    stores_list=[]
     #extract the url of the stores in english
    try:
        if stores:
            for store in stores:
                stores_list.append(store['url_en'])

        else:
            stores_list.append("Unknown")

        logger.info('Successfully converted stores dictionary into a list')

    except Exception as e:
        logger.error("Could not convert stores dictionary to a list, try again", e)
        sys.exit('exit')

    return stores_list



def get_platforms(platforms):
    """Converts parent platform list of dictionaries into list of platforms- simplification
    :param platforms `list`: parent platform list of dictionaries
    :return: list of platforms for each game
    """

    if not isinstance(platforms, list):
        logger.error("platforms is not a list instance")
        sys.exit('exit')

    platforms_list = []

    #extract the platform names
    try:

        if platforms:
            for platform in platforms:
                platforms_list.append(platform['platform']['name'])

        else:
            platforms_list.append('Unknown')

        logger.info('Successfully converted platforms dictionary into a list')

    except Exception as e:
        logger.error("Could not convert platforms dictionary to a list, try again", e)
        sys.exit('exit')

    return platforms_list

def clean_game_titles(title):
    """Removes extra whitespace and quotes
    :param title `str`: game name
    :return: cleaned game name
    """
    if not isinstance(title, str):
        logger.error("title is not a string instance")
        sys.exit('exit')
    #removes spaces and quotes
    title=title.replace(r"'|'","")
    title=title.strip("")
    return title

def encode_features(data,columns_to_encode,columns_to_drop):
    """Encodes features before normalizing and feeding the model
    :param data `dataframe`: cleaned games data
    :param columns_to_encode`list`:columns to be one hot encoded
    :param columns_to_drop `list`: columns with object datatype to be dropped(not scaled)
    :return: featurized dataframe
    """
    if not isinstance(data, pd.DataFrame):
        logger.error("data is not a dataframe instance")
        sys.exit('exit')

    if not isinstance(columns_to_encode, list):
        logger.error("columns_to_encode is not a list instance")
        sys.exit('exit')
    if not isinstance(columns_to_drop, list):
        logger.error("columns_to_drop is not a list instance")
        sys.exit('exit')

    encode_columns=columns_to_encode

    mlb = MultiLabelBinarizer()
    try:

        #one hot encodes list of lists
        genres_df = pd.DataFrame(mlb.fit_transform(data[encode_columns[0]]),columns=mlb.classes_,index=data.index)

        platforms_df = pd.DataFrame(mlb.fit_transform(data[encode_columns[1]]),columns=mlb.classes_,
                                        index=data.index)
        saved_data=data.copy()

        # concatenates the data
        featurized_games=pd.concat([data,genres_df,platforms_df],axis=1)

        #drops non numerical columns
        featurized_games=featurized_games.drop(columns_to_drop,axis=1)

        logger.info('Featurized data is created')

    except Exception as e:
        logger.error(' Could not convert or encode data columns, try again,'
                     'All Columns or some columns to drop do not exist in the dataframe',e)
        sys.exit('exit')


    return featurized_games,saved_data

def scale_features(data):
    """Scales and normalizes the data without the name column
    :param data `dataframe`: dataframe to be normalized and scaled
    :return: Normalized and transformed numpy array ready for modeling
    """
    if not isinstance(data, pd.DataFrame):
        logger.error("data is not a dataframe instance")
        sys.exit('exit')

    scaler=StandardScaler()


    data_featurize=data

    try:
        #scales between 0 and 1
        features=scaler.fit_transform(data_featurize)
        logger.info('Data is standardized')

    except Exception as e:
        logger.error("Could not standardize data",e)
        sys.exit('exit')

    return features

def featurize(data,columns_to_encode,columns_to_drop):
    """Creates features from cleaned data
    :param data `dataframe`: dataframe extract features from
    :param columns_to_encode `list`: List of fields to encode
    :return `array` and `dataframe: features numpy array, intermediate saved data
    """
    if not isinstance(data, pd.DataFrame):
        logger.error("data is not a dataframe instance")
        sys.exit('exit')

    if not isinstance(columns_to_encode,list):
        logger.error("columns_to_encode is not a list instance")
        sys.exit('exit')

    if not isinstance(columns_to_drop,list):
        logger.error("columns_to_drop is not a list instance")
        sys.exit('exit')

    data.genres=data.genres.apply(lambda x:get_genres(x))

    data.parent_platforms=data.parent_platforms.apply(lambda x:get_platforms(x))

    data.stores=data.stores.apply(lambda x:get_stores(x))

    data.name=data.name.apply(lambda x:clean_game_titles(x))

    featurized_data,saved_data=encode_features(data,columns_to_encode=columns_to_encode,columns_to_drop=columns_to_drop)

    features_array=scale_features(featurized_data)

    logger.info('Featurized data is ready to be modeled')

    return features_array,saved_data























