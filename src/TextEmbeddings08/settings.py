from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from tqdm.auto import tqdm
from src.SampleTranslation05.translation_01 import load_samples
tqdm.pandas()
#model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


print("hello")