import pytest
import numpy as np
import logging.config
import implicit
from test.test_functions import test_train_model_helpers


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
    test_array=np.load('./test/test_datasets/features.npy')


    return test_array

def test_happy_compute_similarity():
    """Happy path test checking data type and shapes"""

    test_array=create_data()

    output_array=test_train_model_helpers.compute_similarity(test_array)

    test1 = (type(output_array).__module__ == np.__name__)
    test2 = (output_array.shape[0] == test_array.shape[0])

    assert (test1 and test2)

def test_unhappy_compute_similarity():
    """Unhappy path test checking, passing None to the function"""

    test_array=None

    with pytest.raises(SystemExit):
        output_array = test_train_model_helpers.compute_similarity(test_array)
        assert output_array is None

def test_happy_train_test_split():
    """Happy path test checking, checking datatypes and shapes returned"""
    test_data=create_data()

    size=10
    seed=420

    utility=test_train_model_helpers.compute_similarity(test_data)

    train,test=test_train_model_helpers.train_test_split(utility, size, seed)

    test1=(type(train).__module__ == np.__name__)
    test2=(type(test).__module__ == np.__name__)
    test3=(np.all(train*test)==0)
    test4=(train.shape==test.shape)



    assert(test1 and test2 and test3 and test4)


def test_unhappy_train_test_split():
    """Unhappy path test checking, handling Nones and wrong datatypes"""
    utility = None
    size = 0.1
    seed = 420

    with pytest.raises(SystemExit):
        train, test = test_train_model_helpers.train_test_split(utility, size, seed)
        assert train is None
        assert test is None

def test_happy_train_model():
    """Happy path test checking, checking model datatype"""

    test_data = create_data()

    utility = test_train_model_helpers.compute_similarity(test_data)

    train,test=test_train_model_helpers.train_test_split(utility,size=10,seed=420)
    model = test_train_model_helpers.train_model(train, alpha=15, factors=25, shrinkage=0.1, iterations=50)

    assert(type(model)==implicit.als.AlternatingLeastSquares)

def test_unhappy_train_model():
    """Unhappy path test checking, train_model not given training set"""
    test_data = create_data()

    utility = test_train_model_helpers.compute_similarity(test_data)

    _,_= test_train_model_helpers.train_test_split(utility, size=10, seed=420)

    train=None

    with pytest.raises(SystemExit):
        model=test_train_model_helpers.train_model(train, alpha=15, factors=25,
                                                                   shrinkage=0.1, iterations=50)
        assert model is None


def test_train_model():
    """Wrapper for all the train_model function tests"""

    test_happy_compute_similarity()
    test_unhappy_compute_similarity()
    logger.info('Testing of compute similarity done')

    test_happy_train_test_split()
    test_unhappy_train_test_split()
    logger.info('Testing of train_test_split done')

    test_happy_train_model()
    test_unhappy_train_model()
    logger.info('Testing train_model done')













