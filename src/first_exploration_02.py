import pandas as pd
import numpy as np
import warnings
from typing import Dict, Iterator, Any
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [20, 10]
import os
from tqdm.auto import tqdm

tqdm.pandas()
from enum import StrEnum
from src.data_schemas import OrigDataSchema, MetaDataSchema
import matplotlib.patches as mpatches


def iterate_dataframes(path: str) -> Iterator[pd.DataFrame]:
    """
    Iterates over all .csv files in path as pd.DataFrame
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)
        csvs = [path + x for x in os.listdir(path) if "csv" in x]

        for csv in tqdm(csvs):
            yield pd.read_csv(csv, lineterminator="\n")


def aggregate_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Aggregates dataframe to dict.
    """
    df_la = df.groupby("language").count().reset_index()
    languages = df_la["language"].tolist()
    lang_counts = df_la["username"].tolist()
    df["dupl"] = (
        df.duplicated(subset=OrigDataSchema.TEXT)
        if OrigDataSchema.IS_RETWEET not in df.columns
        else df.duplicated(subset=OrigDataSchema.TEXT) | df[OrigDataSchema.IS_RETWEET]
    )
    languages_dupl = [la + "_dupl" for la in languages]
    lang_dupl_counts = df.groupby("language")["dupl"].sum().tolist()
    unique_user_count = df[OrigDataSchema.USER_ID].unique().shape[0]
    row_count = df.shape[0]
    duplicated_count = df["dupl"].sum()
    date = df.iloc[0][OrigDataSchema.TIMESTAMP][:10]
    aggregation = {
        MetaDataSchema.USERS: unique_user_count,
        MetaDataSchema.ROWS: row_count,
        MetaDataSchema.DUPLICATED: duplicated_count,
        MetaDataSchema.DATE: date,
    }
    aggregation = {
        **dict(zip(languages, lang_counts)),
        **aggregation,
        **dict(zip(languages_dupl, lang_dupl_counts)),
    }
    return aggregation


def aggregate_dataframe_test(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Aggregate DataFrame to check if everything went right.....
    """
    df = df[~df.duplicated(subset="text")]
    df_la = df.groupby("language").count().reset_index()
    languages = df_la["language"].tolist()
    lang_counts = df_la["username"].tolist()
    df["dupl"] = (
        df.duplicated(subset=OrigDataSchema.TEXT)
        if OrigDataSchema.IS_RETWEET not in df.columns
        else df.duplicated(subset=OrigDataSchema.TEXT) | df[OrigDataSchema.IS_RETWEET]
    )
    languages_dupl = [la + "_dupl" for la in languages]
    lang_dupl_counts = df.groupby("language")["dupl"].sum().tolist()
    row_count = df.shape[0]
    duplicated_count = df["dupl"].sum()
    date = df.iloc[0][OrigDataSchema.TIMESTAMP][:10]
    aggregation = {
        MetaDataSchema.ROWS: row_count,
        MetaDataSchema.DUPLICATED: duplicated_count,
        MetaDataSchema.DATE: date,
    }
    aggregation = {
        **dict(zip(languages, lang_counts)),
        **aggregation,
        **dict(zip(languages_dupl, lang_dupl_counts)),
    }
    return aggregation


def exploration_in_numbers(df_agg: pd.DataFrame) -> None:
    """
    Prints general information about aggregated dataframe of tweets.
    """
    for col in [MetaDataSchema.DATE, MetaDataSchema.DUPLICATED, MetaDataSchema.ROWS]:
        if not col in df_agg.columns:
            raise KeyError(f"Key {col} not df.")

    print(f"Tweets total: {df_agg[MetaDataSchema.ROWS].sum()}.")
    print(
        f"First date: {df_agg[MetaDataSchema.DATE].min()}.  Last date: {df_agg[MetaDataSchema.DATE].max()}. Unique dates: {df_agg[MetaDataSchema.DATE].unique().shape[0]}."
    )
    print(
        f"Tweets duplicated or retweeted on the same day total: {df_agg[MetaDataSchema.DUPLICATED].sum()}. Tweets duplicated on the same day percent: {df_agg[MetaDataSchema.DUPLICATED].sum()/df_agg[MetaDataSchema.ROWS].sum() :.2%}"
    )
    print(
        f"Tweets not duplicated or retweeted on the same day total: {df_agg[MetaDataSchema.ROWS].sum()-df_agg[MetaDataSchema.DUPLICATED].sum()}"
    )
    print(
        f"Tweets in a single file on average: {df_agg[MetaDataSchema.ROWS].mean()}, with variance: {df_agg[MetaDataSchema.ROWS].var()} and max: {df_agg[MetaDataSchema.ROWS].max()} and min: {df_agg[MetaDataSchema.ROWS].min()} "
    )


def add_column_others(
    df: pd.DataFrame, languages_to_show: np.ndarray[str]
) -> pd.DataFrame:
    """
    Sums up all not selected languaes and adds them to column other in df.
    """
    languages = np.array(
        [
            "am",
            "ar",
            "bg",
            "bn",
            "ca",
            "ckb",
            "cs",
            "cy",
            "da",
            "de",
            "dv",
            "el",
            "en",
            "es",
            "et",
            "eu",
            "fa",
            "fi",
            "fr",
            "gu",
            "hi",
            "ht",
            "hu",
            "hy",
            "in",
            "is",
            "it",
            "iw",
            "ja",
            "ka",
            "kn",
            "ko",
            "lt",
            "lv",
            "ml",
            "mr",
            "my",
            "ne",
            "nl",
            "no",
            "or",
            "pa",
            "pl",
            "ps",
            "pt",
            "ro",
            "ru",
            "si",
            "sl",
            "sr",
            "sv",
            "ta",
            "te",
            "th",
            "tl",
            "tr",
            "uk",
            "und",
            "ur",
            "vi",
            "zh",
            "sd",
            "km",
            "lo",
            "ug",
            "bo",
        ]
    )
    not_selected_languages = [la for la in languages if not la in languages_to_show]

    df["others"] = df.apply(
        lambda x: sum([x[other] for other in not_selected_languages]), axis=1
    )
    df["others_dupl"] = df.apply(
        lambda x: sum([x[other + "_dupl"] for other in not_selected_languages]), axis=1
    )

    return df


def languages_tabular(df: pd.DataFrame, languages_to_show: np.ndarray[str]) -> None:
    """
    Prints a tabular containing information about all the languages in languages to show
    """
    df = add_column_others(df, languages_to_show)

    languages_to_show = (
        np.append(languages_to_show, "others")
        if not languages_to_show.shape == (66,)
        else languages_to_show
    )
    for la in languages_to_show:
        if not la in df.columns:
            raise KeyError(f"Language: {la} not in df columns.")

    language_counts = np.array([df[la].sum() for la in languages_to_show])

    sorting = np.argsort(language_counts)[::-1]
    language_counts = language_counts[sorting]
    languages_to_show = languages_to_show[sorting]
    language_freqs = np.array(
        [la_count / language_counts.sum() for la_count in language_counts]
    )
    language_dupl = np.array([df[la + "_dupl"].sum() for la in languages_to_show])
    print(f"{'Language'  :10} | {'Count' :>15} | {'Freq' :>10} | {'Dupl %':>10} ")
    for language, count, freq, dupl in zip(
        languages_to_show, language_counts, language_freqs, language_dupl
    ):
        print(
            f"{language  : <10} | {int(count) :15} | {freq :10.2%} | {dupl/count :10.2%}  "
        )


def languages_bar_h(
    df_agg: pd.DataFrame, languages_to_show: np.ndarray[str], save_path: str = None
) -> None:
    """
    Shows count of tweets, percentage of duplicates in a barh graph.
    """

    df_agg = add_column_others(df_agg, languages_to_show)

    languages_to_show = np.append(languages_to_show, "others")

    df = df_agg
    language_counts = np.array([df[la].sum() for la in languages_to_show])

    sorting = np.argsort(language_counts)
    language_counts = language_counts[sorting]
    languages_to_show = languages_to_show[sorting]
    language_dupl = np.array([df[la + "_dupl"].sum() for la in languages_to_show])

    language_counts_dupl = language_counts.copy()

    language_counts = language_counts - language_dupl

    language_freqs = np.array(
        [la_count / language_counts_dupl.sum() for la_count in language_counts_dupl]
    )

    fig, ax = plt.subplots()

    labels = languages_to_show
    ax.barh(labels, language_counts, label=labels[0], left=0)
    ax.barh(labels, language_dupl, label=labels[1], left=language_counts)

    for i, la in enumerate(languages_to_show):
        ax.text(
            (
                language_counts
                + language_dupl
                + 800000 * np.ones(language_dupl.shape[0])
            )[i],
            i,
            f"{language_freqs[i]:10.2%}",
            ha="center",
            va="center",
        )
        ax.text(
            (language_counts)[i],
            i,
            f"{(int(language_counts[i]))} ",
            ha="center",
            va="center",
        )

    orange_patch = mpatches.Patch(color="tab:orange", label="Duplicated")
    blue_patch = mpatches.Patch(color="tab:blue", label="Not Duplicated")
    ax.legend(handles=[orange_patch, blue_patch], loc="lower right")

    ax.set_title("Number of Tweets in Dataset")

    if save_path:
        plt.savefig(save_path)
    plt.show()


def pi_lang_freq(
    df: pd.DataFrame,
    languages: np.ndarray[str],
    save_path: str = None,
    not_dupl: bool = False,
) -> None:
    """
    Sums up the languages in languages in df and shows freqencies in a pie chart.
    """
    for la in languages:
        if not la in df.columns:
            raise KeyError(f"Language: {la} not in df columns.")

    df = add_column_others(df, languages)

    languages = np.append(languages, "others")

    language_counts = [df[la].sum() for la in languages]

    if not_dupl:
        language_counts = [df[la].sum() - df[la + "_dupl"].sum() for la in languages]

    language_freq = np.array(
        [la_co / sum(language_counts) for la_co in language_counts]
    )
    freqs = language_freq
    fig, ax = plt.subplots()
    ax.pie(freqs, labels=languages, autopct="%1.1f%%")

    if save_path:
        plt.savefig(save_path)

    ax.set_title(
        f'Percentage of {"not duplicated" if not_dupl else ""} tweets by language'
    )
    plt.show()


def stackplot_languages_over_weeks(
    df: pd.DataFrame, selected_language: np.ndarray[str], save_path: str = None
) -> None:
    """
    Plots sum over weeks of the aggregated df for each language.
    """

    df = add_column_others(df, selected_language)
    selected_language = np.append(selected_language, "others")

    for la in selected_language:
        if not la in df.columns:
            raise KeyError(f"Language: {la} not in df.columns.")

    if not MetaDataSchema.DATE in df.columns:
        raise KeyError(f"{MetaDataSchema.DATE} not in df.colummns.")

    df["weeks"] = (
        df[MetaDataSchema.DATE]
        .apply(pd.to_datetime)
        .apply(
            lambda x: (
                str(x.year) + "-" + str(x.week)
                if len(str(x.week)) == 2
                else str(x.year) + "-0" + str(x.week)
            )
        )
    )

    df_weeks = df.groupby("weeks")[selected_language].sum()

    fig, ax = plt.subplots()
    index = ["" for _ in range(len(df_weeks.index))]
    index[::4] = list(df_weeks.index)[::4]
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        ax.set_xticklabels(index)

    ax.stackplot(
        df_weeks.index,
        [df_weeks[la] for la in selected_language],
        labels=selected_language,
        alpha=0.8,
    )

    ax.legend(loc="upper left")
    ax.set_title("Number of Tweets in Dataset")
    ax.set_xlabel("Week")

    ax.set_ylabel("Number of Tweets per Week")

    if save_path:
        plt.savefig(save_path)
    plt.show()


def stackplot_duplicates_over_weeks(df: pd.DataFrame, save_path: str = None) -> None:
    """
    Plots sum over weeks of the aggregated df for duplicated and not duplicated columns.
    """

    for col in [MetaDataSchema.ROWS, MetaDataSchema.DUPLICATED]:
        if not col in df.columns:
            raise KeyError(f"Col: {col} not in df.columns.")

    df["weeks"] = (
        df[MetaDataSchema.DATE]
        .apply(pd.to_datetime)
        .apply(
            lambda x: (
                str(x.year) + "-" + str(x.week)
                if len(str(x.week)) == 2
                else str(x.year) + "-0" + str(x.week)
            )
        )
    )

    df_weeks = df.groupby("weeks")[
        [MetaDataSchema.ROWS, MetaDataSchema.DUPLICATED]
    ].sum()
    df_weeks[MetaDataSchema.ROWS] = (
        df_weeks[MetaDataSchema.ROWS] - df_weeks[MetaDataSchema.DUPLICATED]
    )

    fig, ax = plt.subplots()
    ax.stackplot(
        df_weeks.index,
        [df_weeks[MetaDataSchema.ROWS], df_weeks[MetaDataSchema.DUPLICATED]],
        labels=["NOT DUPLICATED", "DUPLICATED"],
        alpha=0.8,
    )

    index = ["" for _ in range(len(df_weeks.index))]
    index[::4] = list(df_weeks.index)[::4]

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        ax.set_xticklabels(index)
    ax.legend(loc="upper left")
    ax.set_title("Number of Tweets in Dataset")
    ax.set_xlabel("Week")
    ax.set_ylabel("Number of Tweets sum per Week")

    if save_path:
        plt.savefig(save_path)
    plt.show()


def stackplot_duplicates_over_weeks_multipl(
    df: pd.DataFrame, languages: np.ndarray[str], save_path: str = None
) -> None:
    """
    Gives multiple stackplot, one for every language provided. Paints duplicates and not duplicates in different colors.
    """
    df = add_column_others(df, languages)

    languages = np.append(languages, "others")

    fig, ax = plt.subplots((languages.shape[0] + 1) // 2, 2)
    fig.tight_layout(pad=1.2)
    for lang_index, language in enumerate(languages):
        x_ind = lang_index // 2
        y_ind = lang_index % 2
        df["weeks"] = (
            df[MetaDataSchema.DATE]
            .apply(pd.to_datetime)
            .apply(
                lambda x: (
                    str(x.year) + "-" + str(x.week)
                    if len(str(x.week)) == 2
                    else str(x.year) + "-0" + str(x.week)
                )
            )
        )

        df_weeks = df.groupby("weeks")[[language, language + "_dupl"]].sum()
        df_weeks[MetaDataSchema.ROWS + "_" + language] = (
            df_weeks[language] - df_weeks[language + "_dupl"]
        )

        ax[x_ind, y_ind].stackplot(
            df_weeks.index,
            [
                df_weeks[MetaDataSchema.ROWS + "_" + language],
                df_weeks[language + "_dupl"],
            ],
            labels=["NOT DUPLICATED", "DUPLICATED"],
            alpha=0.8,
        )
        index = ["" for _ in range(len(df_weeks.index))]
        index[::9] = list(df_weeks.index)[::9]

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            ax[x_ind, y_ind].set_xticklabels(index)  #
        ax[x_ind, y_ind].legend(loc="upper left", fontsize="9")
        ax[x_ind, y_ind].set_title(f"{language}")
    if save_path:
        plt.savefig(save_path)
    plt.show()
