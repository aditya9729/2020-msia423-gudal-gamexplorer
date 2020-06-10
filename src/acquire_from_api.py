import pandas as pd
import numpy as np
import requests
from tqdm import tqdm
from collections import defaultdict
import logging.config
import sys

logging.basicConfig(filename="./config/logging/acquire_from_api.log")
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def acquire_data(source_url,num_pages,page_size_total):
    """Acquires data from endpoint provided by source url
        :param source_url `str`: endpoint url - rawg api database
        :param num_pages `int`: number of pages to extract data from,default is 82(limit)
        :param page_size_total `int`: the number of games on a single page, default is 80(limit)
        :return `list`: Data in the form of a list
    """
    if not isinstance(source_url, str):
        logger.error("Source URL is not a string instance")
        sys.exit('exit')

    if not isinstance(num_pages, int):
        logger.error("Num pages is not an integer instance")
        sys.exit('exit')

    if not isinstance(page_size_total, int):
        logger.error("Page size is not an integer instance")
        sys.exit('exit')

    request_results = []

    #fetches each game from a page, 40 is the limit
    for page in tqdm(range(1,num_pages+1)):

        try:

            url = f"{source_url}?page={page}&page_size={page_size_total}"
            game = requests.get(url)
            logger.info('Received data from enpoint')
        except requests.exceptions.InvalidURL:
            logger.error('Cannot reach endpoint')
            sys.exit('exit')

        try:
            request_results.append(game.json())
            logger.info("Converted raw requests results into json format and add to results list")

        except requests.RequestException as e:
            logger.error("Cannot get jsonified object",e)
            sys.exit('exit')

    return request_results



def data_dictionary(results,num_pages,page_size_extract,column_names):
    """Converts the results list data to a dictonary
        dictionary will be used to render dataframe
        :param results `list`: list of results that are jsonified objects
        :param num_pages `int`: number of pages that have data
        :param page_size_extract `int`: the number of games allowed to extract on a single page, default is 40(limit)
        :param column_names `list`: Field names required
        :return `default dict`: a dictionary with keys as columns values as data
    """
    if not isinstance(results, list):
        logger.error("results is not a list instance")
        sys.exit('exit')

    if not isinstance(num_pages, int):
        logger.error("num_pages is not an integer instance")
        sys.exit('exit')

    if not isinstance(page_size_extract, int):
        logger.error("page_size is not an integer instance")
        sys.exit('exit')

    if not isinstance(column_names, list):
        logger.error("columns is not a list instance")
        sys.exit('exit')



    games_data = defaultdict(list)

    #from acquired results get the required columns
    try:

        for page in tqdm(range(1,num_pages)):

            for game in range(0,page_size_extract):

                for column in column_names:
                    results_render = results[page]['results']
                    games_data[column].append(results_render[game][column])

        logger.info("Raw json data successully converted to a dictionary")
    except IndexError:
        logger.error('Page size does not extend till that index, lower the count')

    return games_data

def games_dataframe(games_dictionary):
    """Converts the games data dictionary into a dataframe
        :param: games_dictionary `dictionary`: a dictionary with keys as columns values as data
        :return `dataframe`: dataframe containing columns and data
    """
    if not isinstance(games_dictionary, dict):
        logger.error("games dictionary is not a dict instance")
        sys.exit('exit')

    #converts a default dictionary instance into a dataframe
    try:

        games = pd.DataFrame(np.array(games_dictionary['name']), columns=['name'])

        for key, value in games_dictionary.items():
            games[key] = np.array(value)

    except Exception as e:
        logger.error('Couldnot convert defaultdict into a dataframe',e)

    return games



