"""
Contains StrEnum classes carrying the names of used fields of pandas dataframes.
"""

from enum import StrEnum


class MetaDataSchema(StrEnum):
    """
    DataSchema for DataFrame created as aggregate over all csvs.
    """
    USERS = "unique_users"
    ROWS = "row_count"
    DUPLICATED = "text_duplicated_count"
    DATE = "date"
    OTHERS = "others"
    DUPLICATED_HASH = "duplicated_hash_count"


class OrigDataSchema(StrEnum):
    """
    DataSchema for the original csvs. 
    """
    IS_RETWEET = "is_retweet"
    TIMESTAMP = "tweetcreatedts"
    ID = "tweetid"
    USER_ID = "userid"
    TEXT = "text"
    LANGUAGE = "language"

    """
    Starting from here are columns that were added later on.
    """

    IS_DUPL = "is_duplicate"


class HashedDataSchema(StrEnum):
    """
    DataSchema for csvs containing hash values for all tweets.
    """
    HASH = "hash"
    ID = "tweetid"
    TIMESTAMP = "tweetcreatedts"
    DATE = "date"


class LanguageMetaDataSchema(StrEnum):
    """
    DataSchema for csvs containting aggregated meta information about the language csvs.
    """

    NOTHING = "yet"

class MinLanguageDataSchema(StrEnum):
    TEXT = "text"
    TIMESTAMP = "tweetcreatedts"
    ID = "tweetid"
    DUPL = "dupl"


class LemmaDataSchema(StrEnum):
    """
    DataSchema for csv containig lemmas, nouns, emojis and so on.
    """

    ID = "tweetid"
    TIMESTAMP = "tweetcreatedts"
    LEMMAS = "lemmas"
    ADJ_VERBS = "adjs_verbs"
    NOUNS = "nouns"
    ENTITIES = "entities"
    EMOJIS = "emojis"