import pandas as pd

from src.utility import iterate_dataframes_path
from collections import Counter

def split_strings_to_list(stringed_list: str) -> list[str]:
    """
    Splits stringed list of dataframe imports into lists.
    """
    if stringed_list=="[]":
        return []
    return stringed_list.strip('[]').replace("'","").split(", ")


def load_and_split_csv(path: str) -> pd.DataFrame:

    df = pd.read_csv(path)

    df = df.assign(
        lemmas = df['lemmas'].apply(split_strings_to_list),
        nouns = df['nouns'].apply(split_strings_to_list),
        adjs_verbs = df['adjs_verbs'].apply(split_strings_to_list),
        emojis = df['emojis'].apply(split_strings_to_list)
    )

    return df



def generate_emoji_counter_for_all_lang()-> dict[str, Counter]:

    counter_dict = {}

    for df, path in iterate_dataframes_path('/Users/robinfeldmann/TopicAnalysisRUWTweets/Data/Lemmas'):
        df = df.assign(
        #lemmas = df['lemmas'].apply(split_strings_to_list),
        #nouns = df['nouns'].apply(split_strings_to_list),
        #adjs_verbs = df['adjs_verbs'].apply(split_strings_to_list),
        emojis = df['emojis'].apply(split_strings_to_list)
    )
        
