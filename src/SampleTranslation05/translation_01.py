from google.cloud import translate
import pandas as pd
from tqdm.auto import tqdm
from src.data_schemas import MinLanguageDataSchema
import numpy as np
tqdm.pandas()

def translate_text(text:str="Hello, world!", project_id: str="evident-display-407715", source_language: str="en-US") -> str:
    """
    Translates text via Google Translate Api from source language to english.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": "en-US",
        }
    )



    return " ".join([transl.translated_text for transl in response.translations])


def translate_text_multiple(list_of_texts:list[str], project_id: str="evident-display-407715", source_language: str="en-US") -> list[str]:
    """
    Translates text via Google Translate Api from source language to english.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": list_of_texts,
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": "en-US",
        }
    )



    return [transl.translated_text for transl in response.translations]


def translate_df(df: pd.DataFrame, source_lang: str, batch_size: int=100) -> pd.Series:
    """
    Translate the text row in a dataframe using translate multiples function.
    """

    translated = []
    for i in tqdm(range(0,df.shape[0], batch_size)):

        listed_data = df['text'][i:i+batch_size].to_list()

        translated += translate_text_multiple(listed_data, source_language= source_lang)
        

    return translated




def create_week_from_timestamp(df: pd.DataFrame, source_name:str = MinLanguageDataSchema.TIMESTAMP) -> pd.Series:
    """
    Creates weeks from timestamps rouw in a dataframe.
    """
    date = df[source_name].astype(str).progress_apply(lambda x: x[:10]).progress_apply(pd.to_datetime)
    return date.progress_apply(lambda x: str(x.year)+ "-" + str(x.week) if len(str(x.week))==2 else str(x.year)+ "-0" + str(x.week))
    

def sample_from_weeks(df: pd.DataFrame, sample_size:int = 100, row_name: str = 'week') -> pd.DataFrame:
    """
    Take sample_size samples from every week in dataframe.
    """
    return df.groupby(row_name).sample(sample_size)


def load_samples(path: str = '/Users/robinfeldmann/TopicAnalysisRUWTweets/src/SampleTranslation05/samples_ready.csv') -> pd.DataFrame:

    df = pd.read_csv(path)

    def listify(series: pd.Series) -> pd.Series:
        return series.str.strip("[]").str.replace(' ','').str.split(',')


    df = df.assign(
        lemmas = df['lemmas'].str.strip("[]").str.replace(' ','').str.replace("'","").str.split(','),
        adjs_verbs= df['adjs_verbs'].str.strip("[]").str.replace(' ','').str.replace("'","").str.split(','),
        nouns = df['nouns'].str.strip("[]").str.replace(' ','').str.replace("'","").str.split(','),
        emojis = df['emojis'].str.strip("[]").str.replace(' ','').str.replace("'",'').str.split(','),
        entities = df['entities'].str.strip("[]").str.replace(' ','').str.replace("'",'').str.split(','),
        translated_lemmas = df['translated_lemmas'].str.strip("[]").str.replace(' ','').str.replace("'","").str.split(','),
        translated_adjs_verbs = df['translated_adjs_verbs'].str.strip("[]").str.replace(' ','').str.replace("'","").str.split(','),
        translated_nouns = df['translated_nouns'].str.strip("[]").str.replace(' ','').str.replace("'","").str.split(','),
        translated_entities = df['translated_entities'].str.strip("[]").str.replace(' ','').str.replace("'",'').str.split(','),
        translated_emojis = df['translated_emojis'].str.strip("[]").str.replace(' ','').str.replace("'",'').str.split(','),

    )

    return df


def load_samples_embedded(path: str = '/Users/robinfeldmann/TopicAnalysisRUWTweets/src/SampleTranslation05/samples_ready.csv') -> pd.DataFrame:

    df = pd.read_csv(path)

    def listify(series: pd.Series) -> pd.Series:
        return series.str.strip("[]").str.replace(' ','').str.split(',')


    df = df.assign(
        lemmas = df['lemmas'].str.strip("[]").str.replace(' ','').str.replace("'","").str.split(','),
        adjs_verbs= df['adjs_verbs'].str.strip("[]").str.replace(' ','').str.replace("'","").str.split(','),
        nouns = df['nouns'].str.strip("[]").str.replace(' ','').str.replace("'","").str.split(','),
        emojis = df['emojis'].str.strip("[]").str.replace(' ','').str.replace("'",'').str.split(','),
        entities = df['entities'].str.strip("[]").str.replace(' ','').str.replace("'",'').str.split(','),
        translated_lemmas = df['translated_lemmas'].str.strip("[]").str.replace(' ','').str.replace("'","").str.split(','),
        translated_adjs_verbs = df['translated_adjs_verbs'].str.strip("[]").str.replace(' ','').str.replace("'","").str.split(','),
        translated_nouns = df['translated_nouns'].str.strip("[]").str.replace(' ','').str.replace("'","").str.split(','),
        translated_entities = df['translated_entities'].str.strip("[]").str.replace(' ','').str.replace("'",'').str.split(','),
        translated_emojis = df['translated_emojis'].str.strip("[]").str.replace(' ','').str.replace("'",'').str.split(','),
        cleaned_text_embeddings = df['cleaned_text_embeddings'].str.encode('utf-8').apply(lambda x: np.frombuffer(x, dtype=np.float32))
    )

    return df