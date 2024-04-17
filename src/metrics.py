from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora.dictionary import Dictionary
import os
import pandas as pd
import numpy as np

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def prepare_coherence_space(
    df: pd.DataFrame, topics: list[int], evaluation_on: str
) -> tuple[list, list]:

    def create_lists(df, on_col="nouns"):

        k = []
        df[on_col].apply(k.extend)

        return k

    df_clustered = pd.DataFrame()
    df_clustered["topics"] = topics

    df_clustered[evaluation_on] = df[evaluation_on].to_list()

    list_of_topics: list[list[str]] = (
        df_clustered.groupby("topics")
        .apply(lambda x: create_lists(x, evaluation_on))
        .to_list()
    )
    list_of_texts: list[list[str]] = df_clustered[evaluation_on]

    return list_of_topics, list_of_texts


def average_coherence(
    topics: list[list[str]], evaluation_space: list[list[str]], top_n=40
) -> float:
    """
    Calculate average coherence score over all topics.
    """
    dic = Dictionary(evaluation_space)
    cm = CoherenceModel(
        topics=topics,
        texts=evaluation_space,
        coherence="c_npmi",
        dictionary=dic,
        topn=top_n,
    )

    coherence_per_topic_score = cm.get_coherence_per_topic()

    return np.mean(coherence_per_topic_score)


def coherence_per_topic(
    topics: list[list[str]], evaluation_space: list[list[str]], top_n=40
) -> list[float]:
    """
    Calculate coherence score for all topics.
    """
    dic = Dictionary(evaluation_space)
    cm = CoherenceModel(
        topics=topics,
        texts=evaluation_space,
        coherence="c_npmi",
        dictionary=dic,
        topn=top_n,
    )

    return cm.get_coherence_per_topic()


def diversity_score(topics: list[list[str]], top_n=40) -> float:
    """
    Calculate diversity score over all topics.
    """
    unique_words = set()
    for topic in topics:
        unique_words = unique_words.union(set(topic[:top_n]))
    td = len(unique_words) / (top_n * len(topics))

    return td


from collections import Counter


def diversity_score_sorted(topics: list[list[str]], top_n=40) -> float:
    """
    Calculate diversity score over all topics.
    """

    ordered_topics = []
    for topic in topics:
        c = Counter()
        c.update(topic)
        ordered_topics.append([x[0] for x in c.most_common(top_n)])

    unique_words = set()
    for topic in ordered_topics:
        unique_words = unique_words.union(set(topic))
    td = len(unique_words) / (top_n * len(topics))

    return td


def coherence_over_multiple_top_words(df, topics, on_column, list_of_top_n):
    """
    Calculate coherence score over different top n words.
    """
    list_of_topics, list_of_texts = prepare_coherence_space(df, topics, on_column)
    return {
        n: average_coherence(list_of_topics, list_of_texts, n) for n in list_of_top_n
    }


def calculate_metrics(
    df: pd.DataFrame, topics: list[int], eval_space_column: str, top_n: int = 40
) -> dict[str, float]:
    """
    Prepare cohencere space and list of topics, then calculate coherence and diversity score and return as dict.
    """
    list_of_topics, list_of_texts = prepare_coherence_space(
        df, topics, eval_space_column
    )

    coherence = average_coherence(list_of_topics, list_of_texts)
    diversity = diversity_score(list_of_topics)

    return {"coherence": coherence, "diversity": diversity}


def calculate_metrics_weighted(
    df: pd.DataFrame, topics: list[int], eval_space_column: str, top_n: int = 40
) -> dict[str, float]:
    """
    Prepare cohencere space and list of topics, then calculate coherence and diversity score and return as dict.
    """
    list_of_topics, list_of_texts = prepare_coherence_space(
        df, topics, eval_space_column
    )
    unique_topics = pd.Series(topics).unique().tolist()

    coherence = coherence_per_topic(list_of_topics, list_of_texts, top_n=top_n)
    diversity_sorted = diversity_score_sorted(list_of_topics, top_n=40)

    topic_series = pd.Series(topics)
    topic_series = topic_series[topic_series != -1]
    scores = pd.Series(
        {topic: score for topic, score in zip(unique_topics, coherence) if topic != -1}
    )

    new_scores = {}

    for topic, weight in (
        (topic_series.value_counts() / topic_series.shape[0]).to_dict().items()
    ):
        new_scores[topic] = weight * scores[topic]

    return {
        "coherence": np.array(list(new_scores.values())).mean(),
        "diversity": diversity_sorted,
    }


def calculate_metrics_weighted_sorted(
    df: pd.DataFrame, topics: list[int], eval_space_column: str, top_n: int = 40
) -> dict[str, float]:
    """
    Prepare cohencere space and list of topics, then calculate coherence and diversity score and return as dict.
    """
    list_of_topics, list_of_texts = prepare_coherence_space(
        df, topics, eval_space_column
    )
    unique_topics = pd.Series(topics).unique().tolist()

    ordered_topics = []
    for topic in list_of_topics:
        c = Counter()
        c.update(topic)
        ordered_topics.append([x[0] for x in c.most_common()])

    coherence = coherence_per_topic(ordered_topics, list_of_texts, top_n=top_n)

    coherence = np.array(coherence)
    coherence[np.isnan(coherence)] = 0

    diversity_sorted = diversity_score(ordered_topics, top_n=40)

    topic_series = pd.Series(topics)
    topic_series = topic_series[topic_series != -1]
    scores = pd.Series(
        {topic: score for topic, score in zip(unique_topics, coherence) if topic != -1}
    )

    new_scores = {}

    for topic, weight in (
        (topic_series.value_counts() / topic_series.shape[0]).to_dict().items()
    ):
        new_scores[topic] = weight * scores[topic]

    return {
        "coherence": np.array(list(new_scores.values())).mean(),
        "diversity": diversity_sorted,
    }
