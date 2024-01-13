

## [0] TOPIC MODELS

David M. Blei, John D. Lafferty

Overview over the fundamentals, linkes to older papers. 
Introduction to LDA and how to calculate it (not important for me).
Introduction to CTM (Correlated Topic Model). Works similiar to LDA but also takes covariance between topics into account. Uses logistic normal distribution instead of dirichlet. Could be better, but is more computional expensive.
Introduction to DMT (dynamic topic model), models development of topics over time.


## [1] Latent Dirichlet Allocation

David M. Blei, Andrew Y. Ng, Michael I. Jordan

Detailed introduction and explanation of LDA. Very deep into probabilistic math.


## [2] Multilingual and Multinidak Topic Modelling with Pretrained Embeddings
15.11.2022

Elainse Zosa, Lidia Pivovarova
Universitiy of Helsinki, Finnlad

Multilingual and Multimodal Topic Modelling
Requieres aligned cocuments like wikipedia articles form multiple languages.




References to older multilingual topic modelling papers:

Mimno et al. 2009
Hao and Paul, 2018
De Semt and Moens 2009
Shi et al 2016
Gutierrez et al 2016

Using word embeddings in topic modelling:
Dieng et al 2020

Conextualised language models:
Bianchi et al 2021
Hoyle et al 20220
Mueller and Dredze 2021
Bianchi et al 2021

Using Bert:
Hoyle et al 2020

Only neural multilingua topic model:
Wu et at 2020


## [3] Sentence-BERT: Sentence Embeddings using SIamese BERT-Networks
27.8.2019
Nils Reimers, Iryna Gurevych
Technische Universität Darmstadt

Builds upon:
BERT: Devlin et al 2018
RoBERTa: Liu et al 2019

Bert calculates semantic similiarity between two senteces. No embeddings. 
SBert adds pooling to the output of BERT/RoBERTa to get fixed length embedding.
Using either the output of the CLS Token(?)/Mean output of all vectors/or max-over-time.
SBert was trained on siamese network structure, by having a training set of fitting pairs and calculating the loss of the output of those pairs embedding after some distance function over the embeddings.


## [4] Principal component analysis: a review and recent developments
Ian T. Jolliffe, Jorge Cadima

University of Exeter, Exeter, UK
19.01.2016

PCA:
How it works,
How it is used,
What are the issues and what are the benefits.

## [5] BERTopic: Neural topic modeling with a class-based TF-IDF procedure
Maarten Grootendorst

11.03.2022


Document Embeddings (SBERT but exchangable with every embedding technique)
Dimensional Reduction (UMAP)
Clustering of semantically similiar documents. (HDBSCAN)
Class based version of TF-IDF?? for topic represantion
(Basicly calculating tf-idf on topics(clustered documents) to get important words for each topic)


Both
datasets were retrieved using OCTIS, and prepro-
cessed by removing punctuation, lemmatization, removing stopwords, and removing documents with
less than 5 words.

Tested on Trumps Tweets. Best performing here was BERTopic-MPNET?

Metrics Used:

Topic Coherence : NPMI: Bouma 2009
-> Lau et al. 2014

Topic diversity:
Dieng et al 2020.
(Percentage of unique words all topics)



## [6] Language-agnostic BERT Sentence Embedding

Fanggxiaoyu Feng, Yinfei Yang, Daniel Cer, Naveen Arivazhag, Wei Wang

Google AI, Mountain View
08.03.2022

## [9] Normalized (Pointwise) Mutual Information in Collocation Extraction

Gerlof Bouma

2009
Department Linguistik, Universität Potsdam

NPMI:

$$ 
NPMI(x,y) = \frac{ln(\frac{p(x,y)}{p(x)p(y)})}{-ln(p(x,y))}
$$

Notice:
no co-occurrences, log𝑝(𝑥,𝑦)→−∞
, so nmpi is -1,
co-occurrences at random, log𝑝(𝑥,𝑦)=log[𝑝(𝑥)𝑝(𝑦)]
, so nmpi is 0,
complete co-occurrences, log𝑝(𝑥,𝑦)=log𝑝(𝑥)=log𝑝(𝑦)
, so nmpi is 1.

