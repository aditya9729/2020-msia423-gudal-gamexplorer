from test.test_featurize import test_featurize
from test.test_train_model import test_train_model
from test.test_score_model import test_score_model
import logging.config

logging.basicConfig(filename="../config/logging/run_tests.log")
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

if __name__=="__main__":

    logger.info('Beginning testing now')
    test_featurize()
    logger.info('test_featurize done')

    test_train_model()
    logger.info('test_train__model done')

    test_score_model()
    logger.info('test_score_model done')

