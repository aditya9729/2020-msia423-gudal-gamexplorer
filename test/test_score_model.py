import pytest
import numpy as np
import logging.config
import joblib
import implicit
from test.test_functions import test_score_model_helpers


logging.basicConfig(filename="./config/logging/run_tests.log")
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

def testing_model():
    """Tesing model required to score it"""

    testing_model=joblib.load('./test/test_model/als_model.joblib')

    return testing_model

def create_data():
    """test test data to score and evaluate the model"""

    test_data=np.load('./test/test_datasets/test.npy')

    return test_data

def test_happy_score_model():
    """Happy test for scoring model checking predictions and model type"""

    model = testing_model()

    predictions=test_score_model_helpers.score_model(model)

    assert (type(model)==implicit.als.AlternatingLeastSquares)
    assert(type(predictions).__module__==np.__name__)

def test_unhappy_score_model():
    """UnHappy test for scoring model, feeding no model to function"""

    model=None

    with pytest.raises(SystemExit):

        predictions=test_score_model_helpers.score_model(model)
        assert predictions is None


def test_happy_evaluate_model():
    """Happy test for evaluating model checking predictions type, metrics is a tuple and 3 metrics returned"""

    test=create_data()
    model = testing_model()

    predictions = test_score_model_helpers.score_model(model)

    metrics=test_score_model_helpers.evaluate_model(pred=predictions,actual=test)

    assert (type(predictions).__module__ == np.__name__)
    assert (type(metrics)==tuple)
    assert(len(metrics)==3)

def test_unhappy_evaluate_model():
    """Unhappy test for evaluating model, giving no predictions to the functions"""

    test = create_data()
    model = testing_model()


    with pytest.raises(SystemExit):
        metrics = test_score_model_helpers.evaluate_model(pred=None, actual=test)

        assert metrics is None

def test_score_model():
    """Wrapper for all the score_model function tests"""

    test_happy_score_model()
    test_unhappy_score_model()
    logger.info('Testing of score_model done')

    test_happy_evaluate_model()
    test_unhappy_evaluate_model()
    logger.info('Testing of evaluate_model done')







