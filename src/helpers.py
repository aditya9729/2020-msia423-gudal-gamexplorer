import pandas as pd
import numpy as np

def filter_on_year(dataframe):
    """
    Used for certain files with release date  as a field
    Filters out those games with release year before 2000
    :param dataframe: dataframe containing release dates of games
    :return dataframe: filtered with the year of each instance in integer format
    """
    #check if any field is release date, or Year
    if np.any(dataframe.columns.str.contains('release_date')):
        date_column = 'release_date'
        dataframe['Year'] = pd.to_datetime(dataframe[date_column]).dt.year.astype('int')

    elif np.any(dataframe.columns.str.contains('Year')):
        dataframe['Year']=dataframe['Year'].astype('int')


    return dataframe[dataframe['Year'] >= 2000]







