import pandas as pd


from src.utility import load_samples_with_numpy, save_csv_with_embeddings

from umap import UMAP


def load_samples(
    path: str = "/Users/robinfeldmann/TopicAnalysisRUWTweets/src/SampleTranslation05/samples_ready.csv",
) -> pd.DataFrame:

    df = pd.read_csv(path)

    df = df[["tweetid", "nouns"]]

    df = df.assign(
        nouns=df["nouns"]
        .str.strip("[]")
        .str.replace(" ", "")
        .str.replace("'", "")
        .str.split(","),
    )

    return df


import os


def load_all_samples():
    dfs = []
    for dir in [
        x
        for x in os.listdir(
            "/Users/robinfeldmann/TopicAnalysisRUWTweets/Data/FinalEmbeddings"
        )
        if not x.endswith(".DS_Store")
    ]:
        path = "/Users/robinfeldmann/TopicAnalysisRUWTweets/Data/FinalEmbeddings/" + dir
        lang = path.split("/")[-1].split("_")[0]
        df_cur = load_samples_with_numpy(path, loading_func=load_samples)
        df_cur["lang"] = lang
        dfs.append(df_cur)
    return pd.concat(dfs)


if __name__ == "__main__":
    df = load_all_samples()
    print("loaded_samples, shape:", df.shape)
    df_sample = df.sample(1000_000)

    umap_model = UMAP(
        n_neighbors=15, n_components=5, min_dist=0.0, metric="cosine", low_memory=True
    )
    trabs = umap_model.fit_transform(df_sample["cleaned_text_embeddings"].to_list())

    df_new = df_sample.copy()
    df_new["min_dim"] = trabs.tolist()

    save_csv_with_embeddings(
        "/Users/robinfeldmann/TopicAnalysisRUWTweets/Data/test",
        df_new[["tweetid", "min_dim", "nouns"]],
        embeddings_columns=["min_dim"],
    )
