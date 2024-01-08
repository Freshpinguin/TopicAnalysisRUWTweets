from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import euclidean
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from tqdm.auto import tqdm
from src.SampleTranslation05.translation_01 import load_samples
tqdm.pandas()

import sys
sys.path.append('/Users/robinfeldmann/Projects/MaximumVarianceUnfolding')
from MVU import MaximumVarianceUnfolding


def visualise_with_dimensional_reduction(df: pd.DataFrame, model: any= PCA(n_components=2), row_to_transform: str="embeddings", hover_data: list[str]=['sentence'], color_to_show: str= None) -> None:

    #pca = PCA(n_components=2)
    min_embeddings = (model.fit_transform(np.array(df[row_to_transform].to_list())))
    x = min_embeddings[:,0]
    y = min_embeddings[:,1]

    x_axis_range = [x.min()-1, x.max()+1]
    y_axis_range = [y.min()-1, y.max()+1]

    fig = px.scatter(df, y=y, x=x,range_x=x_axis_range, range_y=y_axis_range,  hover_data=hover_data, color=color_to_show)
    fig.update_traces(marker_size=10)
    fig.show()


def visualise_with_mvu_reduction(df: pd.DataFrame, row_to_transform: str="embeddings", hover_data: list[str]=['sentence'], color_to_show: str= None ,k =2) -> None:

    model = MaximumVarianceUnfolding()
    min_embeddings = (model.fit_transform(np.array(df[row_to_transform].to_list()), dim=2 , k=k))
    x = min_embeddings[:,0]
    y = min_embeddings[:,1]

    x_axis_range = [x.min()-1, x.max()+1]
    y_axis_range = [y.min()-1, y.max()+1]

    fig = px.scatter(df, y=y, x=x,range_x=x_axis_range, range_y=y_axis_range,  hover_data=hover_data, color=color_to_show)
    fig.update_traces(marker_size=10)
    fig.show()