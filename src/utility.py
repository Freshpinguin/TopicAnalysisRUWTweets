from typing import Iterator, Callable
import pandas as pd
import warnings
from tqdm.auto import tqdm
import os
# register `pandas.progress_apply` and `pandas.Series.map_apply` with `tqdm`
tqdm.pandas()

"""
Contains utility functions that are needed across multiple chapters.
"""


def iterate_dataframes(path: str) -> Iterator[pd.DataFrame]:
    """
    Iterates over all .csv files in path as pd.DataFrame
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)
        csvs = [path + x for x in os.listdir(path) if "csv" in x]
    
        for csv in tqdm(csvs):
            yield pd.read_csv(csv,  lineterminator='\n')



    
def iterate_dataframes_path(path: str) -> Iterator[tuple[pd.DataFrame,str]]:
    """
    Iterates over all .csv files in path as pd.DataFrame
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)
        csvs = [path + x for x in os.listdir(path) if "csv" in x]
    
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
    

def iterate_language_dataframes(path: str) -> Iterator[tuple[pd.DataFrame, str]]:
    """
    Iterates over all .csv files in path as pd.DataFrame and gives name of the language.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)
        csvs = [path + x for x in os.listdir(path) if "csv" in x]
    
        for csv in tqdm(csvs):
            yield pd.read_csv(csv,  lineterminator='\n'), csv.split("/")[-1]


def query_over_all_csvs(lang: str, data_path: str, query_string: str) -> pd.DataFrame:
    """
    Applies a query to every csvs. Then concats the result to a new dataframe.
    """
    dfs = []
    for df in iterate_dataframes(data_path):
        df = df.query(query_string)
        dfs.append(df)
    return pd.concat(dfs)