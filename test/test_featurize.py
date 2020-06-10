import pytest
import numpy as np
import pandas as pd
import logging.config

from test.test_functions import test_featurize_helpers


logging.basicConfig(filename="./config/logging/run_tests.log")
logger = logging.getLogger(__name__)
logger.setLevel("INFO")



def create_data():
    """
        Creates synthetic data for tests
        Returns:
            test_data `dataframe`: testing data randomly generated
            columns_before `list`: list of columns to be used.
    """
    np.random.seed(420)
    test_data=pd.read_pickle('./test/test_datasets/games_data.pkl')

    test_data=test_data.sample(4)
    test_data=test_data.reset_index(drop=True)
    columns_before=test_data.columns


    return test_data, columns_before

def test_happy_get_genres():
    """Happy path test for testing `get_genres` checks dtypes columns and number of rows"""
    test_data,columns=create_data()

    # create feature
    output_genres= test_data.genres.apply(lambda x: test_featurize_helpers.get_genres(x))

    # check datatype, shape and column names
    test1 = (output_genres.dtype == 'object')
    test2 = (output_genres.shape[0] == test_data.shape[0])
    test3 = np.any(test_data.columns.isin(['genres']))
    test4 = ('genres' == output_genres.name)

    assert (test1 and test2 and test3 and test4)

def test_unhappy_get_genres():
    """Unhappy path test for testing `get_genres` with dropping genres"""
    test_data, columns = create_data()

    test_data=test_data.append(pd.Series(dtype='object'), ignore_index=True)

    output_data = test_data.copy()


    # create feature
    with pytest.raises(SystemExit):
        output_data.genres = test_data.genres.apply(lambda x: test_featurize_helpers.get_genres(x))
        assert output_data.genres is None


def test_happy_get_platfroms():
    """Happy path test for testing `get_platforms`"""
    test_data, columns = create_data()

    # create feature
    output_platforms = test_data.parent_platforms.apply(lambda x: test_featurize_helpers.get_platforms(x))

    # check datatype, shape and column names
    test1 = (output_platforms.dtype == 'object')
    test2 = (output_platforms.shape[0] == test_data.shape[0])
    test3 = np.any(test_data.columns.isin(['parent_platforms']))
    test4 = ('parent_platforms' == output_platforms.name)

    assert (test1 and test2 and test3 and test4)


def test_unhappy_get_platfroms():
    """Unhappy path test for testing `get_platforms` with adding missing data"""
    test_data, columns = create_data()

    test_data=test_data.append(pd.Series(dtype='object'), ignore_index=True)


    output_data = test_data.copy()

    # create feature
    with pytest.raises(SystemExit):
        output_data.parent_platforms = test_data.parent_platforms.\
            apply(lambda x: test_featurize_helpers.get_platforms(x))
        assert output_data.parent_platforms is None

def test_happy_get_stores():
    """Happy path test for testing `get_stores`"""
    test_data, columns = create_data()

    # create feature
    output_stores = test_data.stores.apply(lambda x: test_featurize_helpers.get_stores(x))

    # check datatype, shape and column names
    test1 = (output_stores.dtype == 'object')
    test2 = (output_stores.shape[0] == test_data.shape[0])
    test3 = np.any(test_data.columns.isin(['stores']))
    test4 = ('stores'== output_stores.name)

    assert (test1 and test2 and test3 and test4)


def test_unhappy_get_stores():
    """Unhappy path test for testing `get_stores` with stores dropped"""
    test_data, columns = create_data()

    test_data=test_data.append(pd.Series(dtype='object'), ignore_index=True)

    output_data = test_data.copy()

    # create feature
    with pytest.raises(SystemExit):
        output_data.stores = test_data.stores. \
            apply(lambda x: test_featurize_helpers.get_stores(x))
        assert output_data.stores is None

def test_happy_clean_game_titles():
    """Happy path test for testing `game_titles`"""
    test_data, columns = create_data()

    # create feature
    output_game_name = test_data.name.apply(lambda x: test_featurize_helpers.clean_game_titles(x))

    # check datatype, shape and column names
    test1 = (output_game_name.dtype == 'object')
    test2 = (output_game_name.shape[0] == test_data.shape[0])
    test3 = np.any(test_data.columns.isin(['name']))
    test4 = ('name' == output_game_name.name)

    assert (test1 and test2 and test3 and test4)


def test_unhappy_clean_game_titles():
    """Unhappy path test for testing `clean_game_titles` with name dropped"""
    test_data, columns = create_data()

    test_data=test_data.append(pd.Series(dtype='object'), ignore_index=True)

    output_data = test_data.copy()

    # create feature
    with pytest.raises(SystemExit):
        output_data.name = test_data.name.apply(lambda x: test_featurize_helpers.clean_game_titles(x))
        assert output_data.name is None


def test_happy_encode_features():
    """Happy path test for testing `encode_features`"""
    test_data, columns = create_data()

    test_data.genres = test_data.genres.apply(lambda x: test_featurize_helpers.get_genres(x))
    test_data.parent_platforms = test_data.parent_platforms.apply(lambda x: test_featurize_helpers.get_platforms(x))


    columns_to_encode=['genres','parent_platforms']
    columns_to_drop=['name','genres','parent_platforms','stores','background_image','released']
    #encode features
    output_data,intermediate_data= test_featurize_helpers.encode_features(test_data,columns_to_encode=columns_to_encode,
                                                                          columns_to_drop=columns_to_drop)

    # check datatype, shape and column names

    test1 = isinstance(output_data, pd.DataFrame)
    test2 = (output_data.shape[0] == test_data.shape[0])
    test3 = np.any(test_data.columns.isin(columns_to_encode))
    test4= np.any(test_data.columns.isin(columns_to_drop))
    assert (test1 and test2 and test3 and test4)


def test_unhappy_encode_features():
    """UnHappy path test for testing `encode_features`,by dropping columns to encode"""
    test_data, columns = create_data()

    test_data.genres = test_data.genres.apply(lambda x: test_featurize_helpers.get_genres(x))
    test_data.parent_platforms = test_data.parent_platforms.apply(lambda x: test_featurize_helpers.get_platforms(x))

    columns_to_encode = None


    columns_to_drop = ['name', 'genres', 'parent_platforms', 'stores', 'background_image', 'released']

    # create feature
    with pytest.raises(SystemExit):
        output_data, intermediate_data = test_featurize_helpers.encode_features(test_data,
                                                                                columns_to_encode=columns_to_encode,
                                                                                columns_to_drop=columns_to_drop)
        assert output_data is None
        assert intermediate_data is None

def test_happy_scale_features():
    """Happy path test for testing `scale_features`"""
    test_data, columns = create_data()

    columns_to_encode = ['genres', 'parent_platforms']
    columns_to_drop = ['name', 'genres', 'parent_platforms', 'stores', 'background_image', 'released']

    test_data.genres = test_data.genres.apply(lambda x: test_featurize_helpers.get_genres(x))
    test_data.parent_platforms = test_data.parent_platforms.apply(lambda x: test_featurize_helpers.get_platforms(x))

    # encode features
    output_data, intermediate_data =test_featurize_helpers.encode_features(test_data,
                                                                           columns_to_encode=columns_to_encode,
                                                                           columns_to_drop=columns_to_drop)

    scaled_output=test_featurize_helpers.scale_features(output_data)

    # check datatype, shape and column names
    test1 = (type(scaled_output).__module__ == np.__name__ )
    test2 = (scaled_output.shape[0] == test_data.shape[0])
    assert (test1 and test2)




def test_unhappy_scale_features():
    """UnHappy path test for testing `scale_features`,by giving dropping giving a categorical variable as well"""
    test_data, columns = create_data()

    test_data.genres = test_data.genres.apply(lambda x: test_featurize_helpers.get_genres(x))
    test_data.parent_platforms = test_data.parent_platforms.apply(lambda x: test_featurize_helpers.get_platforms(x))

    columns_to_encode = ['genres', 'parent_platforms']

    #haven't dropped name
    columns_to_drop = ['genres', 'parent_platforms', 'stores', 'background_image', 'released']
    # encode features
    output_data, intermediate_data = test_featurize_helpers.encode_features(test_data,
                                                                            columns_to_encode=columns_to_encode,
                                                                            columns_to_drop=columns_to_drop)
    #name has been included to be scaled
    with pytest.raises(SystemExit):
        output_scaled=test_featurize_helpers.scale_features(output_data)
        assert output_scaled is None


def test_featurize():
    """Wrapper to test all functions used for featurizing"""


    test_happy_get_genres()
    test_unhappy_get_genres()
    logger.info('Testing get_genres done')

    test_happy_get_platfroms()
    test_unhappy_get_platfroms()
    logger.info('Testing get_platforms done')

    test_happy_get_stores()
    test_unhappy_get_stores()
    logger.info('Testing get_stores done')

    test_happy_clean_game_titles()
    test_unhappy_clean_game_titles()
    logger.info('Testing clean_game_titles done')

    test_happy_encode_features()
    test_unhappy_encode_features()
    logger.info('Testing encode_features done')

    test_happy_scale_features()
    test_unhappy_scale_features()
    logger.info('Testing scale_features done')






