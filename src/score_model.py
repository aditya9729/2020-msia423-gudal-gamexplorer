from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import logging.config
import sys
import implicit

logging.basicConfig(filename="./config/logging/run_pipeline.log")

logger = logging.getLogger(__name__)

logger.setLevel("INFO")

def score_model(model):
    """Generate predictions for the model as a 2d array
    :param model `joblib object`: Trained ALS model
    :return `array`: 2 dimensional array of predictions
    """
    if type(model)!=implicit.als.AlternatingLeastSquares:
        logger.error('Model is not from the implicit library')
        sys.exit('exit')

    # get predictions
    try:
        item1_latent=model.item_factors
        item2_latent=model.user_factors
        predictions = np.dot(item1_latent, item2_latent.T)

    except Exception as e:
        logger.error("Could not make predictions check latent factors",e)
        sys.exit('exit')

    return predictions

def evaluate_model(pred, actual):
    """Calculates metrics such as mean square error, mean absolute error and root mean square error
    :param pred `array`: 2 dim array of predictions made by the model
    :param actual `array`:2 dim array of testing data
    :return `tuple`: a tuple of the metrics mse, rmse,mae
    """
    if type(pred).__module__ != np.__name__ :
        logger.error("pred is not a numpy array instance")
        sys.exit('exit')

    if type(actual).__module__ != np.__name__ :
        logger.error("actual is not a numpy array instance")
        sys.exit('exit')
    # Ignore nonzero terms.
    pred = pred[actual.nonzero()].flatten()
    actual = actual[actual.nonzero()].flatten()

    #calculate metrics
    mse = mean_squared_error(pred, actual)
    rmse=np.sqrt(mse)
    mae = mean_absolute_error(pred, actual)

    return (mse, rmse,mae)

def save_model_metrics(MODEL_METRICS_PATH,metrics_tuple):
    """Saves model metrics into a text file
    :param MODEL_METRICS_PATH `str`:Path to store the evaluated model metrics
    :param metrics_tuple `tuple`: a tuple of metrics mse, rmse and mae
    :return: None
    """
    mse,rmse,mae=metrics_tuple

    # save metrics in a file
    try:

        with open(MODEL_METRICS_PATH, "w") as f:
            f.write(f"Mean squared error on testing :{mse}")
            f.write("\n")
            f.write(f"Root Mean squared error on testing :{rmse}")
            f.write("\n")
            f.write(f"Mean absolute error on testing :{mae}")
            f.write("\n")
    except Exception as e:
        logger.error("Cannot save metrics, try again")
        sys.exit('exit')




