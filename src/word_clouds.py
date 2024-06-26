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
    sns.set_theme(style="whitegrid")
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
        # axs.title(titles[index])

    plt.axis("off")
    plt.show()
