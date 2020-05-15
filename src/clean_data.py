import pandas as pd
from glob import glob
from src.helpers import filter_on_year
import numpy as np

def read_data(PATH,df_names):
    """
    Reads csv and excel files
    :param str PATH: file path pointing to the directory with the data.
    :return `dict`:a hashmap of pandas dataframes with value as df
    """

    csv_files={}

    #reading csv files

    csv_iterator = glob(PATH+'*.csv')
    for file_idx in range(len(csv_iterator)):
        FILE_PATH=csv_iterator[file_idx]
        csv_files[df_names[file_idx]]=pd.read_csv(FILE_PATH)

    return csv_files


def filter_data(file,ingested_files,cleaned_files):
    """
    1. Drops unnecessary columns
    2. Renames columns
    3. Removes/ Imputes null values
    4. Filters on certain columns, we want games release on and after year 2000
    5. Aggregates by using mean and transformations
    6. Change data types from string to datetime, datetime to int.

    :param file `string key`: A hashmap's keys of datasets/files to be filtered
    :param ingested_files `dict`:A hashmap of keys to datasets as values
    :param cleaned_files `dict`:hashmap to store processed/cleaned data
    :return `dict`: Filtered cleaned files in a hashmap
    """

    if file == 'steam':
        steam_copy = ingested_files['steam'].copy()
        column_names = ['userid','game','action','playtime','redundant']
        steam_copy.columns = column_names
        steam_copy.game = steam_copy.game.apply(lambda x: str(x).strip())
        steam_copy = steam_copy[steam_copy['action'] == 'play']
        steam_copy = steam_copy.drop(['action','redundant'], axis=1)
        steam_copy=steam_copy.rename(columns={'game':'Game'})
        cleaned_files['steam'] = steam_copy


    elif file == 'sales':
        sales_copy = ingested_files['sales'].copy()
        column_names = ['Name','Genre','NA_Sales','EU_Sales','JP_Sales','Other_Sales','Global_Sales']
        platforms=['PC','PS4','PS3','Wii','X360','XOne','WiiU','XB']
        sales_copy=sales_copy[sales_copy['Platform'].isin(platforms)]
        sales_copy=sales_copy.dropna(subset=['Year'])
        sales_copy = filter_on_year(sales_copy)
        sales_copy = sales_copy[column_names]
        sales_copy = sales_copy.rename(columns={'Name': 'Game'})
        sales_copy = sales_copy.groupby('Game', as_index=False).agg({'Genre':'first','NA_Sales':'mean','EU_Sales':'mean',
                                                                    'JP_Sales':'mean','Other_Sales':'mean','Global_Sales':'mean'})
        cleaned_files['sales'] = sales_copy


    elif file == 'metacritic':
        metacritic_copy = ingested_files['metacritic'].copy()
        column_names=['game','genre', 'metascore', 'user_score']
        metacritic_copy = filter_on_year(metacritic_copy)
        metacritic_copy=metacritic_copy[column_names]
        metacritic_copy = metacritic_copy.dropna()
        metacritic_copy = metacritic_copy.rename(columns={'game': 'Game','user_score':'userscore','genre':'Genre'})
        metacritic_copy = metacritic_copy.groupby('Game', as_index=False).agg({'Genre':'first','metascore': 'mean', 'userscore': 'mean'})
        cleaned_files['metacritic'] = metacritic_copy

    return cleaned_files

def save_files(file,CLEAN_PATH,cleaned_files):
    """
    Saves intermediate files in a csv format in the ./data/external path
    :param file `str`: these are cleaned files
    :param CLEAN_PATH `str`: path to clean directory
    :param cleaned_files `dict`: hashmap containing clean data as values
    :return: None
    """
    indices=np.arange(1,cleaned_files[str(file)].shape[0]+1)
    cleaned_files[str(file)]['id']=indices
    cleaned_files[str(file)].to_csv(str(CLEAN_PATH)+'cleaned_'+str(file)+'.csv',index=False)













