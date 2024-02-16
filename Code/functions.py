import warnings
import os
import pandas as pd
def delete_duplicates(df, columns_to_check):
    """
    Check for duplicates in the DataFrame based on specified columns and delete them.
    
    Parameters:
        df (DataFrame): The DataFrame to check for duplicates.
        columns_to_check (list): A list containing the names of columns to use as keys for checking duplicates.
    
    Returns:
        DataFrame: The DataFrame with duplicates removed.
    """
    duplicates = df.duplicated(subset=columns_to_check, keep=False)
    if duplicates.any():
        warnings.warn("Duplicates found and deleted.", UserWarning)
        df.drop_duplicates(subset=columns_to_check, keep='first', inplace=True)
    return df
def read_all_years(database_path):
    '''Read all the csv files in the DataBase folder and return a list of DataFrames
    Parameters:
        database_path (str): The path to the folder containing the csv files.
    Returns:
        list: A list of DataFrames containing the data from the csv files in the DataBase folder.'''
    
    folders = os.listdir(database_path)
    listOfYDf = []
    # Read the csv file in each folder named All_Months_NO2_{year}.csv
    for folder in folders:
        try:
            df = pd.read_csv(f'{database_path}/{folder}/All_Months_NO2_{folder}.csv',sep=';',decimal='.',index_col=0)
            print(f'Folder {folder} read successfully')
            listOfYDf.append(df)
        except:
            print(f'Error reading folder {folder}')
    df_final=pd.concat(listOfYDf, ignore_index=True)
    df_final['date'] = pd.to_datetime(df_final['date'],format='%Y-%m-%d')
    return df_final