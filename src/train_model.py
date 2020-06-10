from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import implicit

import sys
import logging.config

logging.basicConfig(filename="./config/logging/run_pipeline.log")
logger = logging.getLogger(__name__)

logger.setLevel("INFO")

def compute_similarity(feature_array):
    """Generates the Cosine similarity between item features
    :param feature_array: 2 dim array having feature values
    :return cosine_sim_matrix `np.array`: cosine similarity array
    """
    if type(feature_array).__module__ != np.__name__ :
        logger.error("feature_array is not a numpy array")
        sys.exit('exit')
    # generating the cosine similarity matrix
    features=feature_array

    try:
        cosine_sim_matrix = cosine_similarity(features, features)

        logger.info('Cosine similarity of features found')

    except Exception as e:
        logger.error("Could not find cosine similarity for matrix factorization, try again",e)
        sys.exit('exit')

    return cosine_sim_matrix

def train_test_split(utility,size,seed):
    """Creates a train test split within matrix
    The idea is that testing data is masked while training
    :param utility `2d array`: cosine similarity matrix
    :param size int: number of ratings to be masked for each item
    :param seed int: seed for reproducibility
    :return: training and testing arrays
    """
    if type(utility).__module__ != np.__name__:
        logger.error("utility is not a numpy array")
        sys.exit('exit')
    if not isinstance(size,int):
        logger.error("size is not an integer")
        sys.exit('exit')
    if not isinstance(seed,int):
        logger.error("seed is not an integer")
        sys.exit('exit')

    np.random.seed(seed)
    test = np.zeros(utility.shape)
    train = utility.copy()

    try:

        # randomly mask indices in the utility matrix
        for item in range(utility.shape[0]):
            test_ratings = np.random.choice(utility[item, :].nonzero()[0],
                                        size=size,
                                        replace=False)
            train[item, test_ratings] = 0.
            test[item, test_ratings] = utility[item, test_ratings]

        logger.info('Train- Test split successful')

    except Exception as e:

        logger.error('Could not split the data into training and testing',e)
        sys.exit('exit')

    return train, test

def train_model(train,alpha,factors,shrinkage,iterations):
    """Trains an alternative least squares model with cosine matrix factorization
    :param train `array`: training data 2 dim array
    :param alpha `int`: confidence parameter or weightage
    :param factors `int`: number of latent factors to learn
    :param shrinkage `float`: regularization parameter
    :param iterations: Number of iterations to train on
    :return: trained model
    """
    if type(train).__module__ != np.__name__ :
        logger.error("train is not a numpy array instance")
        sys.exit('exit')


    if not isinstance(alpha,int):
        logger.error(f"{alpha} is not an integer instance")
        sys.exit('exit')

    if not isinstance(factors,int):
        logger.error(f"{factors} is not an integer instance")
        sys.exit('exit')

    if not isinstance(shrinkage,float):
        logger.error(f"{shrinkage} is not a float instance")
        sys.exit('exit')

    if not isinstance(iterations,int):
        logger.error(f"{iterations} is not an integer instance")
        sys.exit('exit')

    #create a sparse matrix of train
    train = csr_matrix(train)

    #instantiate model
    model = implicit.als.AlternatingLeastSquares(factors=factors, regularization=shrinkage, iterations=iterations)

    try:

        #weight training confidence = alpha
        train_data = (train * alpha).astype('double')
        model.fit(train_data)
        logger.info('Model training complete')
    except Exception as e:
        logger.error('Model could not be trained, please check',e)
        sys.exit('exit')


    return model

