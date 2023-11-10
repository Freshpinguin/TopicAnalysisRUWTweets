from enum import StrEnum

"""
Contains StrEnum classes carrying the names of used fields of pandas dataframes.
"""

class MetaDataSchema(StrEnum):
    USERS = "unique_users"
    ROWS = "row_count"
    DUPLICATED = "text_duplicated_count"
    DATE = "date"
    OTHERS = "others"


class OrigDataSchema(StrEnum):
    IS_RETWEET = "is_retweet"
    TIMESTAMP = "tweetcreatedts"
    ID = "tweetid"
    USER_ID = "userid"
    TEXT = "text"

    IS_DUPL = "is_duplicate"


class HashedDataSchema(StrEnum):
    HASH = "hash"
    ID = "tweetid"
    TIMESTAMP = "tweetcreatedts"
    DATE = "date"