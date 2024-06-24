import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

plt.rcParams["figure.figsize"] = [20, 10]

from src.word_clouds import wordcloud


def stackplot_topic_counts_over_weeks(df: pd.DataFrame, save_path: str = None) -> None:
    """
    Plots sum over weeks of the aggregated df for each language.
    """

    fig, ax = plt.subplots()
    index = ["" for _ in range(len(df["week"].unique().tolist()))]
    index[::4] = list(df["week"].unique().tolist())[::4]

    ax.stackplot(
        df["week"].unique(),
        [df.query(f"topic=={x}")["count"] for x in df["topic"].unique()],
        labels=["Topic " + str(x) for x in df["topic"].unique()],
        alpha=0.8,
    )
    ax.set_xticklabels(index)
    ax.legend(loc="upper left")
    ax.set_title("Number of Tweets by Topic by Week")
    ax.set_xlabel("Week")

    ax.set_ylabel("Number of Tweets per Week")

    if save_path:
        plt.savefig(save_path)
    plt.show()


def stackplot_topic_counts_over_weeks_relative(
    df: pd.DataFrame, save_path: str = None
) -> None:
    """
    Plots sum over weeks of the aggregated df for each language.
    """

    all_counts = df.groupby("week").sum().reset_index()["count"].values
    fig, ax = plt.subplots()
    index = ["" for _ in range(len(df["week"].unique().tolist()))]
    index[::4] = list(df["week"].unique().tolist())[::4]

    ax.stackplot(
        df["week"].unique(),
        [df.query(f"topic=={x}")["count"] / all_counts for x in df["topic"].unique()],
        labels=["Topic " + str(x) for x in df["topic"].unique()],
        alpha=0.8,
    )
    ax.set_xticklabels(index)
    ax.legend(loc="upper left")
    ax.set_title("Number of Tweets per Topic per Week Normalized")
    ax.set_xlabel("Week")

    ax.set_ylabel("Number of Tweets per Week in % ")

    if save_path:
        plt.savefig(save_path)
    plt.show()


def stackplot_topic_by_language(
    df: pd.DataFrame,
    topic: str,
    save_path: str = None,
) -> None:
    """
    Plots sum over weeks of the aggregated df for each language.
    """

    fig, ax = plt.subplots()
    index = ["" for _ in range(len(df["week"].unique().tolist()))]
    index[::4] = list(df["week"].unique().tolist())[::4]

    all_counts = (
        df.query(f"topic=={topic}")
        .groupby("week")
        .sum()
        .reset_index()["lang_count"]
        .values
    )

    ax.stackplot(
        df["week"].unique(),
        [
            df.query(f"topic=={topic}").query(f"lang=='{x}'")["lang_count"] / all_counts
            for x in df["lang"].unique()
        ],
        labels=[str(x) for x in df["lang"].unique()],
        alpha=0.8,
    )
    ax.set_xticklabels(index)
    ax.legend(loc="upper left")
    ax.set_title(f"Number of Tweets per Language per Week in Percent for Topic {topic}")
    ax.set_xlabel("Week")

    ax.set_ylabel("Number of Tweets per Week")

    if save_path:
        plt.savefig(save_path)
    plt.show()


def stackplot_topic_by_sentiment(
    df: pd.DataFrame,
    topic: str,
    save_path: str = None,
) -> None:
    """
    Plots sum over weeks of the aggregated df for each language.
    """

    fig, ax = plt.subplots()
    index = ["" for _ in range(len(df["week"].unique().tolist()))]
    index[::4] = list(df["week"].unique().tolist())[::4]

    all_counts = (
        df.query(f"topic=={topic}")
        .groupby("week")
        .sum()
        .reset_index()["sentiment_count"]
        .values
    )

    ax.stackplot(
        df["week"].unique(),
        [
            df.query(f"topic=={topic}").query(f"sentiment_label=='{x}'")[
                "sentiment_count"
            ]
            / all_counts
            for x in df["sentiment_label"].unique()
        ],
        labels=[str(x) for x in df["sentiment_label"].unique()],
        alpha=0.8,
    )
    ax.set_xticklabels(index)
    ax.legend(loc="upper left")
    ax.set_title(
        f"Number of Sentiment Labelled Tweets per Week in Percent for Topic {topic}"
    )
    ax.set_xlabel("Week")

    ax.set_ylabel("Number of Sentiment Labelled Tweets per Week")

    if save_path:
        plt.savefig(save_path)
    plt.show()


def topic_in_numbers(topic: str, df_counts, df_lang, df_sentiments):
    tweets = df_counts.query(f"topic=={topic}")["count"].sum()
    relative_tweets = tweets / df_counts["count"].sum()

    tweets_pos = (
        df_sentiments.query(f"topic=={topic}")
        .query("sentiment_label=='positive'")["sentiment_count"]
        .sum()
        / tweets
    )
    tweets_neut = (
        df_sentiments.query(f"topic=={topic}")
        .query("sentiment_label=='neutral'")["sentiment_count"]
        .sum()
        / tweets
    )
    tweets_neg = (
        df_sentiments.query(f"topic=={topic}")
        .query("sentiment_label=='negative'")["sentiment_count"]
        .sum()
        / tweets
    )
    print("Tweets in Topic: ", tweets)
    print(f"Of all tweets: {relative_tweets :10.2%} ")
    print("Of which are:")
    print(f"Positive: {tweets_pos:10.2%}")
    print(f"Neutral: {tweets_neut:10.2%}")
    print(f"Negativ: {tweets_neg:10.2%}")
    print()
    print("Divided in Languages by:")
    lang_dict = {
        lang: df_lang.query(f"topic=={topic}")
        .query(f"lang=='{lang}'")["lang_count"]
        .sum()
        / tweets
        for lang in df_lang["lang"].unique()
    }
    for key, val in lang_dict.items():
        print(f"{key}: {val:10.2%}")


import seaborn as sns
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter


def wordcloud(
    frequencies,
    save_path="",
):
    sns.set_theme(style="whitegrid")
    plt.rcParams["figure.figsize"] = [16, 8]
    wc = WordCloud(
        width=1600,
        height=800,
        background_color="white",
        max_font_size=10000,
        max_words=150,
    )

    wc.generate_from_frequencies(frequencies)

    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    if save_path:
        plt.tight_layout(pad=0)
        plt.savefig(save_path)
    plt.show()


def wordclouds(frequencies: list[Counter], titles: list[str]):
    # sns.set_theme(style="whitegrid")
    plt.rcParams["figure.figsize"] = [25, 40]
    # plt.tight_layout()
    fig, axs = plt.subplots(5, 2)

    for index in range(10):
        x_ind = index // 2
        y_ind = index % 2

        wc = WordCloud(
            width=1600,
            height=800,
            background_color="white",
            max_font_size=10000,
            max_words=100,
        )

        wc.generate_from_frequencies(frequencies[index])
        axs[x_ind, y_ind].imshow(wc, interpolation="bilinear")
        axs[x_ind, y_ind].axis("off")
        axs[x_ind, y_ind].set_title(titles[index])

    plt.axis("off")
    plt.show()


def topic_pi(df_counts):
    fig, ax = plt.subplots()

    labels = df_counts.groupby("topic").sum().reset_index()["topic"]

    freqs = (
        df_counts.groupby("topic").sum()["count"]
        / df_counts.groupby("topic").sum()["count"].sum()
    )
    ax.pie(freqs, labels=labels, autopct="%1.1f%%")

    ax.set_title(f"Relative Topic Size")
    plt.show()
