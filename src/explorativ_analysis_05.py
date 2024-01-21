import pandas as pd

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