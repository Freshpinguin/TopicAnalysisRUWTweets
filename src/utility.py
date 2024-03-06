"""
Contains utility functions that are needed across multiple chapters.
"""
from typing import Iterator, Callable
import pandas as pd
import warnings
from tqdm.auto import tqdm
import os

import pandas as pd
import numpy as np
from src.SampleTranslation05.translation_01 import load_samples
from typing import Callable
# register `pandas.progress_apply` and `pandas.Series.map_apply` with `tqdm`
tqdm.pandas()



def iterate_dataframes(path: str) -> Iterator[pd.DataFrame]:
    """
    Iterates over all .csv files in path as pd.DataFrame
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)
        csvs = [path + x for x in os.listdir(path) if "csv" in x]
    
        for csv in tqdm(csvs):
            yield pd.read_csv(csv,  lineterminator='\n')



    
def iterate_dataframes_path(path: str, supress_tqdm=False) -> Iterator[tuple[pd.DataFrame,str]]:
    """
    Iterates over all .csv files in path as pd.DataFrame
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)
        csvs = [path + x for x in os.listdir(path) if "csv" in x]

        if supress_tqdm:
            for csv in csvs:
                yield pd.read_csv(csv,  lineterminator='\n'), csv
            return 
        for csv in tqdm(csvs):
            yield pd.read_csv(csv,  lineterminator='\n'), csv


def aggregate_data(dir_path: str, target_path: str, aggregate_function: Callable[[pd.DataFrame], dict]) -> pd.DataFrame:
    """
    Creates aggregated data frame and saves it as csv.
    """

    agg_dicts = []
    for df in iterate_dataframes(dir_path):
        agg = aggregate_function(df)
        agg_dicts.append(agg)
    df_agg = pd.DataFrame(agg_dicts).fillna(0)
    df_agg.to_csv(target_path)
    return df_agg

def aggregate_data_path(dir_path: str, target_path: str, aggregate_function: Callable[[pd.DataFrame, str], dict]) -> pd.DataFrame:
    """
    Creates aggregated data frame and saves it as csv.
    """

    agg_dicts = []
    for df, path in iterate_dataframes_path(dir_path):
        agg = aggregate_function(df, path)
        agg_dicts.append(agg)
    df_agg = pd.DataFrame(agg_dicts).fillna(0)
    df_agg.to_csv(target_path)
    return df_agg

def aggregate_data_multiple_rows(dir_path: str, target_path: str, aggregate_function: Callable[[pd.DataFrame], list[dict]]) -> pd.DataFrame:
    """
    Creates aggregated data frame and saves it as csv.
    """

    agg_dicts = []
    for df in iterate_dataframes(dir_path):
        agg = aggregate_function(df)
        agg_dicts.append(agg)

    flatten_dicts = [dic for list_dic in agg_dicts for dic in list_dic]
    df_agg = pd.DataFrame(flatten_dicts).fillna(0)
    df_agg.to_csv(target_path)
    return df_agg
    

def iterate_language_dataframes(path: str) -> Iterator[tuple[pd.DataFrame, str]]:
    """
    Iterates over all .csv files in path as pd.DataFrame and gives name of the language.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)
        csvs = [path + x for x in os.listdir(path) if "csv" in x]
    
        for csv in tqdm(csvs):
            yield pd.read_csv(csv,  lineterminator='\n'), csv.split("/")[-1].split('.')[0]


def query_over_all_csvs(data_path: str, query_string: str) -> pd.DataFrame:
    """
    Applies a query to every csvs. Then concats the result to a new dataframe.
    """
    dfs = []
    for df in iterate_dataframes(data_path):
        df = df.query(query_string)
        dfs.append(df)
    return pd.concat(dfs)




def load_samples_with_numpy(path_to_directory: str, loading_func: Callable[[str], pd.DataFrame] = load_samples) -> pd.DataFrame:
    """
    Loads files with ending csv as pd.Dataframe and then adds every file with ending .npy as column to this dataframe.
    """

    if len([file for file in os.listdir(path_to_directory) if file.endswith('.csv')]) != 1:
        raise OSError("Too many csv files in directory.")
    
    df = load_samples(f"{path_to_directory}/{[file for file in os.listdir(path_to_directory) if file.endswith('.csv')][0]}")
    
    for numpy_file in [file for file in os.listdir(path_to_directory) if file.endswith('.npy')]:
        series = pd.Series(list(np.load(f"{path_to_directory}/{numpy_file}")))

        if series.shape[0] != df.shape[0]:
            raise IndexError("Numpy array and df has different shapes")
        df[numpy_file.split('.')[0]] = series

    return df


def series_numpy_equals(a: pd.Series, b: pd.Series) -> bool:
    """
    Returns if two pd.Series containing numpy array are equal.
    """
    return pd.DataFrame(pd.concat([a.reset_index(drop=True),b.reset_index(drop=True)],axis=1,keys=['emb_1','emb_2'])).reindex().apply(lambda x: np.array_equal(x['emb_1'], x['emb_2']),axis=1).all()



def save_csv_with_embeddings(path_to_dir:str, df: pd.DataFrame, embeddings_columns: list[str], file_name: str = "dataframe.csv"):
    """
    Save dataframe as csv and every column with embeddings as .npy file in directory.
    """
    if not os.path.isdir(path_to_dir):
        os.mkdir(path_to_dir)

    for col in embeddings_columns:
        if not col in df.columns:
            raise AttributeError(f"DataFrame has no row with name {col}")
        
        np.save(f"{path_to_dir}/{col}.npy", np.stack(df[col].to_list()))

    df.drop(embeddings_columns, axis=1).to_csv(f"{path_to_dir}/{file_name}")
