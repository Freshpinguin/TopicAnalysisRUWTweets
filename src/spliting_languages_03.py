from src.data_schemas import OrigDataSchema
import pandas as pd
from src.utility import query_over_all_csvs, iterate_dataframes
import os
import numpy as np
import matplotlib.pyplot as plt
import warnings

def split_csvs_into_language(languages: list[str], data_path: str, target_path: str) -> None:
    """
    Query over all csvs for every language, then saves result in target_path.
    """
    for la in languages:
        
        df = query_over_all_csvs(la, data_path, f"{OrigDataSchema.LANGUAGE} == '{la}'").dropna(subset="text")
        print(la, df.shape)
        df.to_csv(target_path + f"/{la}.csv" )

def splits_csvs_only_english(data_path: str, target_path) -> None:
    """
    Queries all csvs for english tweets. Leaves duplicates out to save ram.
    """
    dfs = []
    i = 0
    for df in iterate_dataframes(data_path):
        df = df.query(f"{OrigDataSchema.LANGUAGE} == 'en'").dropna(subset="text")
        df = df[~(df.duplicated(subset=OrigDataSchema.TEXT) if  OrigDataSchema.IS_RETWEET not in df.columns else df.duplicated(subset=OrigDataSchema.TEXT) | df[OrigDataSchema.IS_RETWEET])]
        dfs.append(df)
        if len(dfs) > 250:
            pd.concat(dfs).to_csv(target_path + f"/en_{i}.csv")
            dfs = []
            i = i+ 1
    pd.concat(dfs).to_csv(target_path + f"/en_{i}.csv")


def language_csvs_quick_stats(data_path: str) -> None:
    """
    Print some quick stats about the files.
    """
    file_sizes = [os.stat(data_path+"/" + path).st_size/ (1024 * 1024) for path in  os.listdir(data_path)]
    file_names = [x.split('.')[0] for x in os.listdir(data_path)]

    for name, size in zip(file_names, file_sizes):
        print(f"{name}: {size:10.10} mb")


def aggregate_languages(df: pd.DataFrame) -> dict:
    """
    Aggregates a dataframe containing info about one language to a single column.
    """
    df['dupl'] = df.duplicated(subset=OrigDataSchema.TEXT) if  OrigDataSchema.IS_RETWEET not in df.columns else df.duplicated(subset=OrigDataSchema.TEXT) | df[OrigDataSchema.IS_RETWEET]

    dupl_count = df['dupl'].sum()
    count = df.shape[0]

    lang = df[OrigDataSchema.LANGUAGE].unique()[0]
    unique_dates = df[OrigDataSchema.TIMESTAMP].unique().shape[0]

    return {"la": lang,
            "count" :count,
            "dupl_count": dupl_count,
            "dates": unique_dates}

def aggregate_languages_weeks(df: pd.DataFrame, agg_dict:dict) -> dict:
    """
    Aggregates a dataframme containing info about one language to a column per week.
    """

    if not agg_dict:
        agg_dict = {OrigDataSchema.ID: 'count',
                                        'dupl': 'sum'}

    df['dupl'] = df.duplicated(subset=OrigDataSchema.TEXT) if  OrigDataSchema.IS_RETWEET not in df.columns else df.duplicated(subset=OrigDataSchema.TEXT) | df[OrigDataSchema.IS_RETWEET]

    df['weeks'] = df[OrigDataSchema.TIMESTAMP].apply(pd.to_datetime).apply(lambda x: str(x.year)+ "-" + str(x.week) if len(str(x.week))==2 else str(x.year)+ "-0" + str(x.week))

    df_weeks = df.groupby('weeks').agg(agg_dict)
    
    return df_weeks
